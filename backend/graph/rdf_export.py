from __future__ import annotations

from typing import Any, Dict, List

from rdflib import Graph, Literal, Namespace, RDF, RDFS, XSD


def _safe_uri_fragment(value: str) -> str:
    return (
        value.strip()
        .replace(" ", "_")
        .replace("/", "_")
        .replace(":", "_")
        .replace("#", "_")
        .replace(".", "_")
    )


def export_graph_to_turtle(nodes: List[Dict[str, Any]], rels: List[Dict[str, Any]]) -> str:
    g = Graph()
    NG = Namespace("https://neurograph.dev/ontology/")

    g.bind("ng", NG)
    g.bind("rdfs", RDFS)
    g.bind("xsd", XSD)

    uri_by_id: Dict[str, Any] = {}
    labels_by_id: Dict[str, List[str]] = {}

    for n in nodes:
        node_id = str(n["id"])
        labels = n.get("labels") or []
        props = n.get("properties") or {}

        u = NG[_safe_uri_fragment(node_id)]
        uri_by_id[node_id] = u
        labels_by_id[node_id] = labels

        if labels:
            # Use the first label as rdf:type for simplicity
            g.add((u, RDF.type, NG[_safe_uri_fragment(labels[0])]))
        g.add((u, RDFS.label, Literal(node_id.replace("_", " ").title())))

        for k, v in props.items():
            if k in ("embedding",):
                continue
            pred = NG[_safe_uri_fragment(k)]
            if isinstance(v, bool):
                g.add((u, pred, Literal(v, datatype=XSD.boolean)))
            elif isinstance(v, int):
                g.add((u, pred, Literal(v, datatype=XSD.integer)))
            elif isinstance(v, float):
                g.add((u, pred, Literal(v, datatype=XSD.double)))
            else:
                g.add((u, pred, Literal(str(v))))

    for r in rels:
        s = str(r["source"])
        t = str(r["target"])
        rel_type = str(r["type"])
        su = uri_by_id.get(s, NG[_safe_uri_fragment(s)])
        tu = uri_by_id.get(t, NG[_safe_uri_fragment(t)])

        predicate = NG[_safe_uri_fragment(rel_type.lower())]
        g.add((su, predicate, tu))

        props = r.get("properties") or {}
        # Emit relationship properties as reified statements (simple blank node)
        if props:
            bn = NG[f"stmt_{_safe_uri_fragment(s)}_{_safe_uri_fragment(rel_type)}_{_safe_uri_fragment(t)}"]
            g.add((bn, RDF.type, NG.Statement))
            g.add((bn, NG.subject, su))
            g.add((bn, NG.predicate, predicate))
            g.add((bn, NG.object, tu))
            for k, v in props.items():
                pred = NG[_safe_uri_fragment(k)]
                if isinstance(v, bool):
                    g.add((bn, pred, Literal(v, datatype=XSD.boolean)))
                elif isinstance(v, int):
                    g.add((bn, pred, Literal(v, datatype=XSD.integer)))
                elif isinstance(v, float):
                    g.add((bn, pred, Literal(v, datatype=XSD.double)))
                else:
                    g.add((bn, pred, Literal(str(v))))

    return g.serialize(format="turtle")

