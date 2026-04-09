from __future__ import annotations

from typing import Any, Dict, List


def normalize_records(records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Demo-normalization: lowercases keys and trims string values.
    """
    out: List[Dict[str, Any]] = []
    for r in records:
        nr: Dict[str, Any] = {}
        for k, v in r.items():
            nk = str(k).strip().lower()
            if isinstance(v, str):
                nv: Any = v.strip()
            else:
                nv = v
            nr[nk] = nv
        out.append(nr)
    return out

