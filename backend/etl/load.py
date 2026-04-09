from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from graph.neo4j_client import Neo4jClient


async def clear_graph(db: Neo4jClient) -> None:
    await db.run_query("MATCH (n) DETACH DELETE n")


async def upsert_relationship(
    db: Neo4jClient,
    src_label: str,
    src_name: str,
    rel_type: str,
    tgt_label: str,
    tgt_name: str,
    props: Dict[str, Any],
) -> None:
    await db.run_query(
        f"""
        MATCH (a:{src_label} {{name: $src}})
        MATCH (b:{tgt_label} {{name: $tgt}})
        MERGE (a)-[r:{rel_type}]->(b)
        SET r += $props
        """,
        {"src": src_name, "tgt": tgt_name, "props": props},
    )


async def upsert_evidence_support(
    db: Neo4jClient,
    doi: str,
    src_name: str,
    rel_type: str,
    tgt_name: str,
) -> None:
    # Neo4j relationships can't be relationship endpoints. We encode "supports this connection"
    # as evidence linking to the source node with properties describing the supported relationship.
    await db.run_query(
        """
        MATCH (e:ClinicalEvidence {doi: $doi})
        MATCH (s {name: $src})
        MERGE (e)-[r:SUPPORTS]->(s)
        SET r.finding = $finding,
            r.rel_type = $rel_type,
            r.target = $tgt
        """,
        {
            "doi": doi,
            "src": src_name,
            "tgt": tgt_name,
            "rel_type": rel_type,
            "finding": f"Supports {src_name} -[{rel_type}]-> {tgt_name}",
        },
    )


async def load_relationships(
    db: Neo4jClient,
    indicates: Iterable[Tuple[str, str, str, Dict[str, Any]]],
    associated: Iterable[Tuple[str, str, str, Dict[str, Any]]],
    comorbid: Iterable[Tuple[str, str, str, Dict[str, Any]]],
    risk: Iterable[Tuple[str, str, str, Dict[str, Any]]],
) -> None:
    for src, rel, tgt, props in indicates:
        await upsert_relationship(db, "Biomarker", src, rel, "Symptom", tgt, props)
    for src, rel, tgt, props in associated:
        await upsert_relationship(db, "Symptom", src, rel, "Condition", tgt, props)
    for src, rel, tgt, props in comorbid:
        await upsert_relationship(db, "Condition", src, rel, "Condition", tgt, props)
        await upsert_relationship(db, "Condition", tgt, rel, "Condition", src, props)
    for src, rel, tgt, props in risk:
        await upsert_relationship(db, "RiskFactor", src, rel, "Condition", tgt, props)


async def get_metrics(db: Neo4jClient) -> Dict[str, Any]:
    return await db.get_graph_stats()

