from __future__ import annotations

from typing import List

from graph.neo4j_client import Neo4jClient


CONSTRAINTS: List[str] = [
    "CREATE CONSTRAINT biomarker_name_unique IF NOT EXISTS FOR (n:Biomarker) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT symptom_name_unique IF NOT EXISTS FOR (n:Symptom) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT condition_name_unique IF NOT EXISTS FOR (n:Condition) REQUIRE n.name IS UNIQUE",
    "CREATE CONSTRAINT evidence_doi_unique IF NOT EXISTS FOR (n:ClinicalEvidence) REQUIRE n.doi IS UNIQUE",
    "CREATE CONSTRAINT riskfactor_name_unique IF NOT EXISTS FOR (n:RiskFactor) REQUIRE n.name IS UNIQUE",
]

INDEXES: List[str] = [
    "CREATE INDEX biomarker_category IF NOT EXISTS FOR (n:Biomarker) ON (n.category)",
    "CREATE INDEX condition_icd IF NOT EXISTS FOR (n:Condition) ON (n.icd_code)",
    "CREATE INDEX evidence_year IF NOT EXISTS FOR (n:ClinicalEvidence) ON (n.year)",
]


async def create_schema(db: Neo4jClient) -> None:
    for c in CONSTRAINTS:
        await db.run_query(c)
    for i in INDEXES:
        await db.run_query(i)

