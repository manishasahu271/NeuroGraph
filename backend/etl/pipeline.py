from __future__ import annotations

from typing import Any, Dict

from graph.neo4j_client import Neo4jClient
from graph.schema import create_schema

from .dedup import dedup_and_upsert_node
from .load import clear_graph, get_metrics, load_relationships, upsert_evidence_support
from .seed_data import (
    ASSOCIATED_WITH_RELS,
    BIOMARKERS,
    CLINICAL_EVIDENCE,
    COMORBID_RELS,
    EVIDENCE_SUPPORTS,
    INDICATES_RELS,
    CONDITIONS,
    RISK_FACTORS,
    RISK_FACTOR_RELS,
    SYMPTOMS,
)


async def run_seed_pipeline(db: Neo4jClient) -> Dict[str, Any]:
    await clear_graph(db)
    await create_schema(db)

    for b in BIOMARKERS:
        await dedup_and_upsert_node(
            db,
            label="Biomarker",
            unique_field="name",
            unique_value=b["name"],
            props=b,
            embed_text_input=f"{b['name']} {b.get('description','')}",
        )

    for s in SYMPTOMS:
        await dedup_and_upsert_node(
            db,
            label="Symptom",
            unique_field="name",
            unique_value=s["name"],
            props=s,
            embed_text_input=f"{s['name']} {s.get('description','')}",
        )

    for c in CONDITIONS:
        await dedup_and_upsert_node(
            db,
            label="Condition",
            unique_field="name",
            unique_value=c["name"],
            props=c,
            embed_text_input=f"{c['name']} {c.get('description','')}",
        )

    for e in CLINICAL_EVIDENCE:
        props = dict(e)
        doi = props.pop("doi")
        props["doi"] = doi
        await dedup_and_upsert_node(
            db,
            label="ClinicalEvidence",
            unique_field="doi",
            unique_value=doi,
            props=props,
            embed_text_input=None,
        )

    for rf in RISK_FACTORS:
        await dedup_and_upsert_node(
            db,
            label="RiskFactor",
            unique_field="name",
            unique_value=rf["name"],
            props=rf,
            embed_text_input=f"{rf['name']} {rf.get('category','')}",
        )

    await load_relationships(db, INDICATES_RELS, ASSOCIATED_WITH_RELS, COMORBID_RELS, RISK_FACTOR_RELS)

    for doi, rels in EVIDENCE_SUPPORTS:
        for (src, rel, tgt) in rels:
            await upsert_evidence_support(db, doi=doi, src_name=src, rel_type=rel, tgt_name=tgt)

    metrics = await get_metrics(db)
    return {"status": "ok", "metrics": metrics}

