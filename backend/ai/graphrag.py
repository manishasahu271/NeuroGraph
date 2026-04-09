from __future__ import annotations

import json
import re
from typing import Any, Dict, List, Optional, Tuple

from config import settings
from graph.neo4j_client import Neo4jClient

from .prompts import ANSWER_GENERATION_PROMPT, CYPHER_GENERATION_PROMPT


# Fallback: map user language → Symptom.name values in the graph
SYMPTOM_KEYWORDS: Dict[str, List[str]] = {
    "fatigue": [
        "weak",
        "weakness",
        "feeling weak",
        "tired",
        "exhausted",
        "low energy",
        "fatigue",
        "drained",
        "sluggish",
        "lethargic",
    ],
    "memory_lapses": [
        "forget",
        "forgetful",
        "memory",
        "remember",
        "recall",
        "losing track",
        "forgetting",
    ],
    "attention_deficit": [
        "focus",
        "concentrate",
        "distracted",
        "attention",
        "scatterbrained",
        "can't focus",
    ],
    "mood_changes": ["sad", "moody", "irritable", "emotional", "depressed", "down", "mood"],
    "sleep_disturbance": [
        "insomnia",
        "can't sleep",
        "cant sleep",
        "awake at night",
        "restless night",
        "sleepless",
        "trouble sleeping",
        "poor sleep",
    ],
    "social_withdrawal": [
        "lonely",
        "isolated",
        "antisocial",
        "withdrawn",
        "avoiding people",
        "social withdrawal",
    ],
    "psychomotor_slowing": ["slow", "clumsy", "uncoordinated", "reaction time"],
    "word_finding_difficulty": [
        "can't find words",
        "tip of tongue",
        "word finding",
        "forget words",
    ],
    "anhedonia": ["don't enjoy", "lost interest", "nothing fun", "bored with everything"],
    "restlessness": ["anxious", "restless", "nervous", "on edge", "can't sit still", "worried"],
    "concentration_difficulty": ["brain fog", "foggy", "unclear thinking", "confusion"],
    "executive_function_decline": ["planning", "organizing", "can't decide", "overwhelmed by tasks"],
    "decision_making_difficulty": ["indecisive", "can't choose", "paralyzed by choices"],
    "emotional_blunting": ["numb", "feel nothing", "emotionless", "flat"],
    "spatial_disorientation": ["lost", "navigation", "directions", "disoriented"],
}

# Keywords → Biomarker.name (for questions about specific digital signals)
BIOMARKER_KEYWORDS: List[Tuple[str, List[str]]] = [
    (
        "typing_speed_decline",
        ["typing speed", "typing", "keystroke", "keyboard", "type slower", "declining typing"],
    ),
    ("typing_error_increase", ["typos", "typing error", "mistypes"]),
    ("keystroke_rhythm_irregularity", ["keystroke rhythm", "keystroke"]),
    ("sleep_fragmentation", ["fragmented sleep", "sleep fragmentation", "tossing"]),
    ("sleep_onset_delay", ["sleep onset", "can't fall asleep", "late bedtime"]),
    ("nighttime_phone_usage", ["midnight phone", "phone at night"]),
    ("circadian_rhythm_shift", ["circadian", "sleep schedule"]),
    ("reduced_daily_mobility", ["steps", "mobility", "walking less", "not leaving"]),
    ("gait_irregularity", ["gait", "walking pattern"]),
    ("increased_app_switching", ["app switching", "switching apps"]),
    ("scrolling_passivity_increase", ["scrolling", "passive scrolling"]),
    ("screen_time_spike", ["screen time"]),
    ("social_interaction_decline", ["social isolation", "fewer calls", "messages"]),
    ("voice_prosody_change", ["voice", "prosody"]),
    ("word_finding_pauses", ["pauses speaking", "mid-sentence pause"]),
    ("location_entropy_decrease", ["fewer places", "staying home"]),
    ("response_time_increase", ["slow to respond", "notifications"]),
    ("phone_unlock_frequency_change", ["unlock phone", "checking phone"]),
    ("exercise_decline", ["exercise", "workout", "activity"]),
    ("heart_rate_variability_decrease", ["hrv", "heart rate variability"]),
]


def match_symptoms(question: str) -> List[str]:
    q = question.lower()
    matched: List[str] = []
    for symptom, keywords in SYMPTOM_KEYWORDS.items():
        if any(kw in q for kw in keywords):
            matched.append(symptom)
    return matched


def match_biomarker_names(question: str) -> List[str]:
    q = question.lower()
    out: List[str] = []
    for name, keywords in BIOMARKER_KEYWORDS:
        if any(kw in q for kw in keywords):
            out.append(name)
    return sorted(set(out))


def _clean_cypher(text: str) -> str:
    t = text.strip()
    t = re.sub(r"^```(?:cypher)?", "", t, flags=re.IGNORECASE).strip()
    t = re.sub(r"```$", "", t).strip()
    return t


def _path_cypher_with_params() -> str:
    """Paths with explicit relationship props; empty list means 'do not filter' on that axis."""
    return """
    MATCH (b:Biomarker)-[r1:INDICATES]->(s:Symptom)-[r2:ASSOCIATED_WITH]->(c:Condition)
    WHERE (size($symptoms) = 0 OR s.name IN $symptoms)
      AND (size($biomarkers) = 0 OR b.name IN $biomarkers)
    OPTIONAL MATCH (e:ClinicalEvidence)-[sup:SUPPORTS]->(b)
    WHERE sup IS NULL OR (sup.rel_type = 'INDICATES' AND sup.target = s.name)
    RETURN b.name AS biomarker,
           s.name AS symptom,
           c.name AS condition,
           r1.strength AS strength,
           r2.correlation AS correlation,
           (coalesce(r1.strength, 0.0) + coalesce(r2.correlation, 0.0)) / 2.0 AS confidence,
           collect(DISTINCT e) AS evidence
    ORDER BY strength DESC, correlation DESC
    LIMIT 24
    """


def _fallback_cypher(question: str) -> Tuple[str, Dict[str, Any]]:
    q = question.lower()
    biomarkers = match_biomarker_names(q)
    symptoms = match_symptoms(q)

    # Narrow conditions when user names a disease theme
    extra_symptoms: List[str] = []
    if any(k in q for k in ["alzheimer", "alzheimer's", "dementia", "mci", "cognitive decline"]):
        extra_symptoms.extend(["memory_lapses", "word_finding_difficulty", "executive_function_decline"])
    if any(k in q for k in ["depress", "sad", "hopeless"]):
        extra_symptoms.extend(["mood_changes", "anhedonia"])
    if "anxious" in q or "anxiety" in q or "worried" in q:
        extra_symptoms.append("restlessness")
    if "can't sleep" in q or "cant sleep" in q or ("sleep" in q and "can't" in q):
        extra_symptoms.append("sleep_disturbance")

    symptoms = sorted(set(symptoms + extra_symptoms))

    # Typing / biomarker-focused questions: filter by biomarker, not random symptoms
    if biomarkers:
        return _path_cypher_with_params(), {"symptoms": [], "biomarkers": biomarkers}

    # Symptom-matched questions (e.g. "feeling weak" → fatigue)
    if symptoms:
        return _path_cypher_with_params(), {"symptoms": symptoms, "biomarkers": []}

    # Keyword-only heuristics when no symptom keyword matched
    if "typing" in q or "keystroke" in q or "keyboard" in q:
        return _path_cypher_with_params(), {
            "symptoms": [],
            "biomarkers": ["typing_speed_decline", "typing_error_increase", "keystroke_rhythm_irregularity"],
        }
    if "sleep" in q and any(x in q for x in ["can't", "cant", "insomnia", "awake", "fragment"]):
        return _path_cypher_with_params(), {"symptoms": ["sleep_disturbance"], "biomarkers": []}

    # Safe default when nothing matched
    return _path_cypher_with_params(), {"symptoms": ["fatigue", "mood_changes"], "biomarkers": []}


async def _llm_generate_cypher(question: str) -> Optional[str]:
    if not settings.openai_api_key:
        return None
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate

        llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key, temperature=0)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", CYPHER_GENERATION_PROMPT),
            ]
        )
        msg = prompt.format_messages(question=question)
        resp = await llm.ainvoke(msg)
        return _clean_cypher(resp.content)
    except Exception:
        return None


async def _llm_generate_answer(question: str, graph_results: Dict[str, Any]) -> Optional[str]:
    if not settings.openai_api_key:
        return None
    try:
        from langchain_openai import ChatOpenAI
        from langchain_core.prompts import ChatPromptTemplate

        llm = ChatOpenAI(model="gpt-4o-mini", api_key=settings.openai_api_key, temperature=0.2)
        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", ANSWER_GENERATION_PROMPT),
            ]
        )
        msg = prompt.format_messages(
            question=question,
            graph_results=json.dumps(graph_results, ensure_ascii=False),
        )
        resp = await llm.ainvoke(msg)
        return str(resp.content).strip()
    except Exception:
        return None


def _node_name(node: Any) -> str:
    if node is None:
        return ""
    try:
        if hasattr(node, "get"):
            return str(node.get("name") or node.get("doi") or node.get("title") or "")
    except Exception:
        pass
    if isinstance(node, dict):
        return str(node.get("name") or node.get("doi") or node.get("title") or "")
    return str(getattr(node, "name", "") or "")


def _float_prop(obj: Any, key: str, default: float = 0.0) -> float:
    """Read a numeric property from dict or Neo4j graph object."""
    if obj is None:
        return default
    v: Any = None
    if isinstance(obj, dict):
        v = obj.get(key)
    else:
        try:
            v = obj[key]
        except Exception:
            try:
                if hasattr(obj, "get"):
                    v = obj.get(key)
            except Exception:
                v = None
    if v is None:
        return default
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _row_to_path(r: Dict[str, Any]) -> Dict[str, Any]:
    """One result row → path dict with strength, correlation, confidence."""
    if "biomarker" in r and r.get("biomarker") is not None:
        biomarker = str(r.get("biomarker") or "")
        symptom = str(r.get("symptom") or "")
        condition = str(r.get("condition") or "")
        if "strength" in r:
            strength = _float_prop(r, "strength")
        elif "indicates_strength" in r:
            strength = _float_prop(r, "indicates_strength")
        else:
            strength = 0.0
        if "correlation" in r:
            correlation = _float_prop(r, "correlation")
        elif "association_correlation" in r:
            correlation = _float_prop(r, "association_correlation")
        else:
            correlation = 0.0
        conf_raw = r.get("confidence")
        if conf_raw is not None:
            try:
                confidence = float(conf_raw)
            except (TypeError, ValueError):
                confidence = (strength + correlation) / 2.0
        else:
            confidence = (strength + correlation) / 2.0
    else:
        b = r.get("b")
        s = r.get("s")
        c = r.get("c")
        i = r.get("i") or r.get("r1")
        a = r.get("a") or r.get("r2")
        biomarker = _node_name(b)
        symptom = _node_name(s)
        condition = _node_name(c)
        strength = _float_prop(i, "strength")
        correlation = _float_prop(a, "correlation")
        confidence = (strength + correlation) / 2.0

    return {
        "biomarker": biomarker,
        "symptom": symptom,
        "condition": condition,
        "strength": round(strength, 4),
        "correlation": round(correlation, 4),
        "confidence": round(float(confidence), 4),
    }


def _diversify_paths_by_symptom(paths: List[Dict[str, Any]], limit: int = 8) -> List[Dict[str, Any]]:
    """Prefer a mix of symptoms when many paths exist (e.g. sleep + anxiety)."""
    if not paths or limit <= 0:
        return paths
    by_symptom: Dict[str, List[Dict[str, Any]]] = {}
    for p in paths:
        sym = str(p.get("symptom") or "")
        by_symptom.setdefault(sym, []).append(p)
    for lst in by_symptom.values():
        lst.sort(key=lambda x: float(x.get("confidence") or 0.0), reverse=True)
    out: List[Dict[str, Any]] = []
    keys = sorted(by_symptom.keys(), key=lambda k: (-len(by_symptom[k]), k))
    idx = 0
    while len(out) < limit and any(by_symptom.values()):
        progressed = False
        for k in keys:
            bucket = by_symptom.get(k) or []
            if idx < len(bucket):
                out.append(bucket[idx])
                progressed = True
                if len(out) >= limit:
                    return out
        if not progressed:
            break
        idx += 1
    return out


def _extract_paths(rows: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    paths = [_row_to_path(r) for r in rows]
    evidence_map: Dict[str, Dict[str, Any]] = {}
    for r in rows:
        ev_coll = r.get("evidence")
        if not ev_coll:
            continue
        for e in ev_coll:
            if e is None:
                continue
            try:
                props = dict(e)
            except Exception:
                props = e if isinstance(e, dict) else {}
            doi = str(props.get("doi") or "")
            if doi and doi not in evidence_map:
                evidence_map[doi] = {
                    "title": props.get("title", ""),
                    "doi": doi,
                    "journal": props.get("journal", ""),
                    "year": int(props.get("year", 0) or 0),
                    "summary": props.get("summary", ""),
                }
    evidence = list(evidence_map.values())
    evidence.sort(key=lambda x: (x.get("year", 0), x.get("doi", "")), reverse=True)
    return paths, evidence


def _rule_based_answer(question: str, paths: List[Dict[str, Any]], evidence: List[Dict[str, Any]]) -> str:
    if not paths:
        return (
            "I couldn’t find a strong match in the current knowledge graph for that question. "
            "Try asking about specific biomarkers like typing speed, sleep fragmentation, social interaction decline, "
            "or conditions like early Alzheimer’s, depression, anxiety, insomnia, ADHD, or Parkinson’s.\n\n"
            "Disclaimer: this is for research purposes only."
        )

    top = paths[:3]
    biomarker_list = ", ".join(sorted({p["biomarker"] for p in top if p.get("biomarker")})) or "the matched biomarkers"
    condition_list = ", ".join(sorted({p["condition"] for p in top if p.get("condition")})) or "the matched conditions"
    evidence_bits = ""
    if evidence:
        ev = evidence[:3]
        evidence_bits = " Supported by: " + "; ".join([f"{e['journal']} ({e['year']}), DOI {e['doi']}" for e in ev]) + "."

    return (
        f"Based on the knowledge graph, {biomarker_list} are connected to symptoms and conditions such as {condition_list}. "
        "Key reasoning paths are listed below, with confidence derived from relationship strength/correlation where available."
        f"{evidence_bits}\n\nDisclaimer: this is for research purposes only."
    )


def _keyword_routing_prefers_fallback(question: str) -> bool:
    """
    When the question clearly maps to known symptoms or biomarker themes, use the
    deterministic parameterized query so we always return relationship props (strength/correlation)
    and correct node filters. LLM Cypher is kept for broader questions without keyword hits.
    """
    return bool(match_symptoms(question) or match_biomarker_names(question))


async def answer_question(db: Neo4jClient, question: str) -> Dict[str, Any]:
    params: Optional[Dict[str, Any]] = None
    cypher: Optional[str] = None

    if settings.openai_api_key and not _keyword_routing_prefers_fallback(question):
        cypher = await _llm_generate_cypher(question)

    if not cypher:
        cypher, params = _fallback_cypher(question)

    rows = await db.run_query(cypher, params)
    paths, evidence = _extract_paths(rows)

    # If we used LLM Cypher (broad questions) but got no paths or no relationship scores, retry with deterministic routing
    if not _keyword_routing_prefers_fallback(question) and (
        not paths or all(float(p.get("confidence") or 0) == 0.0 for p in paths)
    ):
        fb_cypher, fb_params = _fallback_cypher(question)
        fb_rows = await db.run_query(fb_cypher, fb_params)
        fb_paths, fb_evidence = _extract_paths(fb_rows)
        if fb_paths and any(float(x.get("confidence") or 0) > 0 for x in fb_paths):
            paths, evidence = fb_paths, fb_evidence

    paths_out = _diversify_paths_by_symptom(paths, 8)
    graph_results = {"paths": paths_out, "evidence": evidence[:8]}
    answer = await _llm_generate_answer(question, graph_results)
    if not answer:
        answer = _rule_based_answer(question, paths_out, evidence)

    return {"answer": answer, "paths": paths_out, "evidence": evidence[:10]}
