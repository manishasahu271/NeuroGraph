from __future__ import annotations

from pydantic import BaseModel, Field
from fastapi import APIRouter, Request

from ai.graphrag import answer_question

router = APIRouter(tags=["query"])


class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, max_length=2000)


@router.post("/query")
async def query(req: QueryRequest, request: Request):
    db = request.app.state.db
    return await answer_question(db, req.question)

