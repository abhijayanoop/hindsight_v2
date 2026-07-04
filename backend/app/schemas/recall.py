"""Request/response models for querying incident memory (api/v1/routers/recall.py)."""

from typing import Any

from pydantic import BaseModel, Field


class RecallRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Natural-language question or incident description.")
    dataset: str | None = Field(
        default=None, description="Override the tenant's default Cognee dataset."
    )
    search_type: str = Field(
        default="GRAPH_COMPLETION",
        description="Name of a cognee.SearchType member, e.g. GRAPH_COMPLETION, CHUNKS, TEMPORAL.",
    )
    top_k: int = Field(default=15, ge=1, le=100)


class RecallResult(BaseModel):
    content: Any = Field(description="Raw result payload returned by Cognee for this hit.")
    score: float | None = None
    source: str | None = None


class RecallResponse(BaseModel):
    query: str
    search_type: str
    results: list[RecallResult]
