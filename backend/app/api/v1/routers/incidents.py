"""Incident CRUD + ingestion. STUB (Day 1) below `services/incident_service.py`.

Tenant scoping is hardcoded to a nil UUID until auth lands — every call
path is already shaped for `tenant_id` to come from `get_current_user`.
"""

from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.incident import IncidentCreate, IncidentIngestResponse, IncidentRead
from app.services.incident_service import incident_service

router = APIRouter(prefix="/incidents", tags=["incidents"])

_STUB_TENANT_ID = UUID(int=0)  # STUB (Day 1): replace with current_user.tenant_id


@router.post("", response_model=IncidentIngestResponse, status_code=status.HTTP_201_CREATED)
async def create_incident(payload: IncidentCreate) -> IncidentIngestResponse:
    try:
        incident = await incident_service.create_incident(payload, tenant_id=_STUB_TENANT_ID)
    except NotImplementedError:
        raise HTTPException(
            status.HTTP_501_NOT_IMPLEMENTED, "Incident ingestion is not implemented yet."
        )
    return IncidentIngestResponse(incident=incident, cognified=False)


@router.get("/{incident_id}", response_model=IncidentRead)
async def get_incident(incident_id: UUID) -> IncidentRead:
    try:
        return await incident_service.get_incident(incident_id, tenant_id=_STUB_TENANT_ID)
    except NotImplementedError:
        raise HTTPException(
            status.HTTP_501_NOT_IMPLEMENTED, "Incident lookup is not implemented yet."
        )


@router.get("", response_model=list[IncidentRead])
async def list_incidents() -> list[IncidentRead]:
    try:
        return await incident_service.list_incidents(tenant_id=_STUB_TENANT_ID)
    except NotImplementedError:
        raise HTTPException(
            status.HTTP_501_NOT_IMPLEMENTED, "Incident listing is not implemented yet."
        )
