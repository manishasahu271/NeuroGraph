from __future__ import annotations

from typing import Any, Dict, List


def ingest_raw(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    In a real system, this would read device logs / uploads.
    For this production demo, the ingest step accepts a JSON payload and returns a list of records.
    """
    records = payload.get("records")
    if isinstance(records, list):
        return [r for r in records if isinstance(r, dict)]
    return []

