"""
FastAPI application entry-point.

Creates all database tables on startup via Base.metadata.create_all()
and exposes a GET /health endpoint for smoke-testing.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.core.db import Base, engine

# Import all models so Base.metadata knows about every table.
from app.models import domain as _models  # noqa: F401

from app.schemas.domain import HealthResponse


# ── Lifespan (replaces deprecated @app.on_event) ────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create tables that don't exist yet.
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: nothing to tear down for now.


# ── App ──────────────────────────────────────────────────────────────────────

settings = get_settings()

app = FastAPI(
    title="Autism Bias Research API",
    description="Backend for the multi-agent simulation platform studying implicit autism-related bias in LLMs.",
    version="0.1.0",
    lifespan=lifespan,
)

# Allow the Next.js frontend (default dev port 3000) to call us.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


from app.simulation.router import router as simulation_router
from app.features.router import router as features_router
from app.classifier.router import router as classifier_router
from app.bias.router import router as bias_router

# ── Routes ───────────────────────────────────────────────────────────────────

app.include_router(simulation_router)
app.include_router(features_router)
app.include_router(classifier_router)
app.include_router(bias_router)




@app.get("/health", response_model=HealthResponse, tags=["meta"])
async def health_check():
    """Basic liveness probe."""
    return HealthResponse(status="ok", environment=settings.APP_ENV)

