from __future__ import annotations

from fastapi import APIRouter, Request

from etl.pipeline import run_seed_pipeline

router = APIRouter(tags=["etl"])


@router.post("/ingest")
async def ingest(request: Request):
    db = request.app.state.db
    result = await run_seed_pipeline(db)
    return result

