from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Query, Request, Response

from graph.rdf_export import export_graph_to_turtle

router = APIRouter(tags=["graph"])


def _human_label(name: str) -> str:
    return name.replace("_", " ").title()


def _props_from_neo4j_node(n: Any) -> Dict[str, Any]:
    """Neo4j Node maps to property dict; fall back for driver edge cases."""
    if n is None:
        return {}
    if isinstance(n, dict):
        return dict(n)
    if hasattr(n, "items"):
        return dict(n.items())
    return dict(n)


def _node_id_and_eid(n: Any) -> tuple[str, str]:
    props = _props_from_neo4j_node(n)
    eid = ""
    if hasattr(n, "element_id"):
        eid = str(n.element_id)
    nid = props.get("name") or props.get("doi") or eid
    return (str(nid) if nid is not None else "", eid)


def _api_node_label(group: str, nid: str, props: Dict[str, Any]) -> str:
    """Human-readable label; avoid raw DOI strings on ClinicalEvidence nodes."""
    if group == "ClinicalEvidence":
        journal = props.get("journal") or ""
        year = props.get("year")
        if journal and year is not None and str(year).strip():
            return f"{journal} {year}"
        title = (props.get("title") or "").strip()
        if title:
            parts = title.split()
            head = " ".join(parts[:5])
            return f"{head}…" if len(parts) > 5 else head
        tail = str(nid).split("/")[-1]
        return f"Study {tail}"
    return _human_label(nid)


@router.get("/graph")
async def get_graph(request: Request, node: Optional[str] = Query(default=None)):
    db = request.app.state.db

    if node:
        # ClinicalEvidence nodes use `doi`; others use `name`. Match either so subgraph focus works.
        # Split nodes vs rels: the old single-query UNWIND on relationships(p) dropped all rows when
        # paths were missing or rel lists were empty, so the client got no nodes back.
        anchor_rows = await db.run_query(
            """
            MATCH (n)
            WHERE n.name = $anchor OR n.doi = $anchor
            OPTIONAL MATCH p = (n)-[*1..2]-(m)
            WITH collect(DISTINCT n) + collect(DISTINCT m) AS raw
            UNWIND raw AS nn
            WITH collect(DISTINCT nn) AS nodes
            RETURN [x IN nodes WHERE x IS NOT NULL] AS nodes
            """,
            {"anchor": node},
        )
        if not anchor_rows or not anchor_rows[0].get("nodes"):
            return {"nodes": [], "links": []}
        nodes: List[Any] = anchor_rows[0]["nodes"] or []

        rel_rows = await db.run_query(
            """
            MATCH (n)
            WHERE n.name = $anchor OR n.doi = $anchor
            OPTIONAL MATCH p = (n)-[*1..2]-(m)
            WITH collect(DISTINCT p) AS paths
            UNWIND [path IN paths WHERE path IS NOT NULL] AS path
            UNWIND relationships(path) AS r
            RETURN collect(DISTINCT r) AS rels
            """,
            {"anchor": node},
        )
        rels: List[Any] = []
        if rel_rows and rel_rows[0].get("rels") is not None:
            rels = rel_rows[0]["rels"] or []

        api_nodes = []
        for n in nodes:
            props = _props_from_neo4j_node(n)
            nid, _eid = _node_id_and_eid(n)
            lbls = list(getattr(n, "labels", []) or [])
            group = lbls[0] if lbls else "Node"
            api_nodes.append(
                {
                    "id": nid,
                    "label": _api_node_label(group, nid, props),
                    "group": group,
                    "description": props.get("description") or props.get("summary") or "",
                    "properties": props,
                }
            )
        api_links = []
        for r in rels:
            props = dict(r) if hasattr(r, "items") else {}
            src_id, _ = _node_id_and_eid(r.start_node)
            tgt_id, _ = _node_id_and_eid(r.end_node)
            api_links.append(
                {
                    "source": src_id,
                    "target": tgt_id,
                    "type": r.type,
                    "properties": props,
                }
            )
        return {"nodes": api_nodes, "links": api_links}

    nodes = await db.get_all_nodes()
    rels = await db.get_all_relationships()

    api_nodes = []
    for n in nodes:
        props = n["properties"]
        nid = str(n["id"])
        labels = n.get("labels") or []
        group = labels[0] if labels else "Node"
        api_nodes.append(
            {
                "id": nid,
                "label": _api_node_label(group, nid, props),
                "group": group,
                "description": props.get("description") or props.get("summary") or "",
                "properties": props,
            }
        )

    api_links = [
        {
            "source": r["source"],
            "target": r["target"],
            "type": r["type"],
            "properties": r.get("properties") or {},
        }
        for r in rels
    ]

    return {"nodes": api_nodes, "links": api_links}


@router.get("/stats")
async def stats(request: Request) -> Dict[str, Any]:
    db = request.app.state.db
    return await db.get_graph_stats()


@router.get("/rdf")
async def rdf(request: Request):
    db = request.app.state.db
    nodes = await db.get_all_nodes()
    rels = await db.get_all_relationships()
    turtle = export_graph_to_turtle(nodes, rels)
    return Response(content=turtle, media_type="text/turtle; charset=utf-8")

