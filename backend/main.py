from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from graph.neo4j_client import Neo4jClient
from routes import graph, health, ingest, query

db = Neo4jClient()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    app.state.db = db
    yield
    await db.close()


app = FastAPI(title="NeuroGraph API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in settings.cors_origins.split(",") if o.strip()],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(query.router, prefix="/api")
app.include_router(graph.router, prefix="/api")
app.include_router(health.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")
