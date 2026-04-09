from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from neo4j import AsyncGraphDatabase, AsyncDriver

from config import settings


@dataclass
class Neo4jClient:
    driver: Optional[AsyncDriver] = None

    async def connect(self) -> None:
        if self.driver is not None:
            return
        self.driver = AsyncGraphDatabase.driver(
            settings.neo4j_uri,
            auth=(settings.neo4j_user, settings.neo4j_password),
            max_connection_pool_size=50,
        )
        await self.driver.verify_connectivity()

    async def close(self) -> None:
        if self.driver is None:
            return
        await self.driver.close()
        self.driver = None

    async def run_query(self, cypher: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if self.driver is None:
            raise RuntimeError("Neo4j driver not connected")
        async with self.driver.session() as session:
            result = await session.run(cypher, params or {})
            rows = await result.data()
            return rows

    async def get_all_nodes(self) -> List[Dict[str, Any]]:
        rows = await self.run_query(
            """
            MATCH (n)
            RETURN elementId(n) AS eid, labels(n) AS labels, properties(n) AS props
            """
        )
        out: List[Dict[str, Any]] = []
        for r in rows:
            props = dict(r["props"] or {})
            node_id = props.get("name") or props.get("doi") or r["eid"]
            out.append(
                {
                    "id": str(node_id),
                    "labels": r["labels"],
                    "properties": props,
                }
            )
        return out

    async def get_all_relationships(self) -> List[Dict[str, Any]]:
        rows = await self.run_query(
            """
            MATCH (a)-[r]->(b)
            RETURN
              elementId(a) AS a_eid,
              elementId(b) AS b_eid,
              type(r) AS type,
              properties(r) AS props,
              properties(a) AS a_props,
              properties(b) AS b_props
            """
        )
        out: List[Dict[str, Any]] = []
        for r in rows:
            a_props = dict(r["a_props"] or {})
            b_props = dict(r["b_props"] or {})
            source = a_props.get("name") or a_props.get("doi") or r["a_eid"]
            target = b_props.get("name") or b_props.get("doi") or r["b_eid"]
            out.append(
                {
                    "source": str(source),
                    "target": str(target),
                    "type": r["type"],
                    "properties": dict(r["props"] or {}),
                }
            )
        return out

    async def get_node_by_name(self, name: str) -> Dict[str, Any]:
        rows = await self.run_query(
            """
            MATCH (n {name: $name})
            OPTIONAL MATCH (n)-[r]-(m)
            RETURN properties(n) AS node, labels(n) AS labels,
                   collect({rel: type(r), relProps: properties(r), other: properties(m), otherLabels: labels(m)}) AS neighbors
            """,
            {"name": name},
        )
        if not rows:
            return {"node": None, "labels": [], "neighbors": []}
        row = rows[0]
        neighbors = [x for x in row["neighbors"] if x.get("other") is not None and x.get("rel") is not None]
        return {
            "node": dict(row["node"] or {}),
            "labels": row["labels"] or [],
            "neighbors": neighbors,
        }

    async def get_graph_stats(self) -> Dict[str, Any]:
        node_counts = await self.run_query(
            """
            MATCH (n)
            UNWIND labels(n) AS l
            RETURN l AS label, count(*) AS count
            ORDER BY count DESC
            """
        )
        rel_counts = await self.run_query(
            """
            MATCH ()-[r]->()
            RETURN type(r) AS type, count(*) AS count
            ORDER BY count DESC
            """
        )
        totals = await self.run_query(
            """
            MATCH (n)
            WITH count(n) AS nodes
            MATCH ()-[r]->()
            RETURN nodes AS nodes, count(r) AS relationships
            """
        )
        return {
            "totals": totals[0] if totals else {"nodes": 0, "relationships": 0},
            "nodes_by_label": node_counts,
            "relationships_by_type": rel_counts,
        }

