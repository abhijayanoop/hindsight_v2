"""Feedback on recall quality, and the belief-revision (forget/retract) primitive.

Request models live inline here rather than in `schemas/` since this
router's shapes are small and specific to it; see `schemas/recall.py` for
the pattern used by larger, reused shapes.
"""

from uuid import UUID

from fastapi import APIRouter
from pydantic import BaseModel, Field

from app.services.cognee_service import cognee_service

router = APIRouter(prefix="/feedback", tags=["feedback"])


class FeedbackCreate(BaseModel):
    """Signal on a recall result: was it relevant, or should a fact be corrected?"""

    query: str
    result_ref: str | None = Field(default=None, description="Opaque reference to the recalled item.")
    is_relevant: bool | None = None
    correction: str | None = Field(default=None, description="Free-text correction / belief revision note.")


class ForgetRequest(BaseModel):
    dataset: str | None = None
    data_id: UUID | None = None
    everything: bool = False


@router.post("", status_code=202)
async def submit_feedback(payload: FeedbackCreate) -> dict:
    """Record feedback on a recall result.

    STUB (Day 1): should persist feedback in our own DB and feed it into
    Cognee's self-improvement loop (`cognee.improve` / `feedback_influence`
    on search) rather than just acknowledging receipt.
    """
    return {"received": True, "query": payload.query}


@router.post("/forget")
async def forget_fact(payload: ForgetRequest) -> dict:
    """Retract a fact from memory — the belief-revision primitive.

    E.g. correcting a misattributed incident cause so dependent graph
    reasoning (recurrence links, derived prevention rules) updates.
    """
    return await cognee_service.forget(
        dataset=payload.dataset,
        data_id=payload.data_id,
        everything=payload.everything,
    )
