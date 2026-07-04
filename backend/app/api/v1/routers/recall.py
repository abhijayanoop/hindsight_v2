"""Query incident memory."""

from fastapi import APIRouter

from app.schemas.recall import RecallRequest, RecallResponse, RecallResult
from app.services.cognee_service import cognee_service

router = APIRouter(prefix="/recall", tags=["recall"])


@router.post("", response_model=RecallResponse)
async def recall_incidents(payload: RecallRequest) -> RecallResponse:
    """Query incident memory via Cognee's graph/vector search."""
    results = await cognee_service.recall(
        query=payload.query,
        dataset=payload.dataset,
        search_type=payload.search_type,
        top_k=payload.top_k,
    )
    return RecallResponse(
        query=payload.query,
        search_type=payload.search_type,
        results=[RecallResult(content=result) for result in results],
    )
