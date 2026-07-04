"""Raw knowledge graph inspection/visualization."""

from fastapi import APIRouter, Query

from app.services.cognee_service import cognee_service

router = APIRouter(prefix="/graph", tags=["graph"])


@router.get("")
async def get_graph(dataset: str | None = Query(default=None)) -> dict:
    """Return the knowledge graph for a dataset, for visualization/inspection."""
    graph = await cognee_service.get_graph(dataset=dataset)
    return {"dataset": dataset, "graph": graph}
