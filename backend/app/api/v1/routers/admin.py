"""Admin-only operations: memory reset and rule derivation (memify).

Both routes are gated behind `require_role("admin")`, which is itself a
stub (see `dependencies.py`) — this demonstrates the pattern every
protected route should follow once real auth lands, even though calling
these endpoints today returns 501.
"""

from fastapi import APIRouter, Depends

from app.dependencies import CurrentUser, require_role
from app.services.cognee_service import cognee_service

router = APIRouter(prefix="/admin", tags=["admin"])


@router.post("/reset")
async def reset_memory(current_user: CurrentUser = Depends(require_role("admin"))) -> dict:
    """Wipe all Cognee graph/vector/cache state. Destructive."""
    await cognee_service.reset()
    return {"status": "reset"}


@router.post("/memify")
async def run_memify(
    dataset: str | None = None,
    current_user: CurrentUser = Depends(require_role("admin")),
) -> dict:
    """Derive durable PreventionRules from repeated incident patterns in `dataset`."""
    await cognee_service.memify(dataset=dataset)
    return {"status": "memify complete", "dataset": dataset}
