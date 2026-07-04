"""Request/response models for incident CRUD + ingestion (api/v1/routers/incidents.py)."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class IncidentCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    text: str = Field(..., min_length=1, description="Full incident write-up, fed to cognee.add().")
    occurred_at: datetime | None = Field(
        default=None, description="When the incident happened, for temporal_cognify ordering."
    )
    tags: list[str] = []


class IncidentRead(BaseModel):
    id: UUID
    tenant_id: UUID
    title: str
    text: str
    occurred_at: datetime | None
    tags: list[str] = []
    created_at: datetime

    model_config = {"from_attributes": True}


class IncidentIngestResponse(BaseModel):
    incident: IncidentRead
    cognified: bool = Field(description="Whether cognify has been (re)run over the dataset yet.")
