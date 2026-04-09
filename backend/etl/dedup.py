from __future__ import annotations

from typing import Any, Dict, Optional, Tuple

import numpy as np

from ai.embeddings import embed_text
from graph.neo4j_client import Neo4jClient


def _cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = (np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0:
        return 0.0
    return float(np.dot(a, b) / denom)


async def dedup_and_upsert_node(
    db: Neo4jClient,
    label: str,
    unique_field: str,
    unique_value: str,
    props: Dict[str, Any],
    embed_text_input: Optional[str],
    threshold: float = 0.85,
) -> Tuple[str, bool]:
    """
    Returns (resolved_unique_value, merged_into_existing).

    For seed entities, we treat `name` as unique_field for most nodes.
    If a similar existing node is found (cosine sim > threshold), we merge props into it
    instead of creating a new node.
    """
    # If this node type has a hard unique identity (e.g., doi), don't dedup beyond that.
    if unique_field in ("doi",):
        cypher = f"""
        MERGE (n:{label} {{ {unique_field}: $uv }})
        SET n += $props
        """
        await db.run_query(cypher, {"uv": unique_value, "props": props})
        return unique_value, False

    embedding = None
    if embed_text_input:
        embedding = embed_text(embed_text_input)

    if embedding is not None:
        rows = await db.run_query(
            f"""
            MATCH (n:{label})
            WHERE n.embedding IS NOT NULL
            RETURN n.{unique_field} AS uv, n.embedding AS embedding
            """,
        )
        best_uv = None
        best_sim = -1.0
        a = np.array(embedding, dtype=np.float32)
        for r in rows:
            b = np.array(r["embedding"], dtype=np.float32)
            sim = _cosine(a, b)
            if sim > best_sim:
                best_sim = sim
                best_uv = r["uv"]

        if best_uv is not None and best_sim >= threshold:
            cypher = f"""
            MATCH (n:{label} {{ {unique_field}: $best }})
            SET n += $props
            """
            await db.run_query(cypher, {"best": best_uv, "props": props})
            return str(best_uv), True

    props_to_set = dict(props)
    if embedding is not None:
        props_to_set["embedding"] = embedding

    cypher = f"""
    MERGE (n:{label} {{ {unique_field}: $uv }})
    SET n += $props
    """
    await db.run_query(cypher, {"uv": unique_value, "props": props_to_set})
    return unique_value, False

