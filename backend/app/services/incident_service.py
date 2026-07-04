"""Incident business logic: validation, tenant scoping, and orchestration
around `cognee_service`.

STUB: routes currently call this with the shape they'll need later, but
the logic itself (dedup, dataset-per-tenant resolution, write-through to
our own audit log) is not implemented yet.
"""

from uuid import UUID

from app.schemas.incident import IncidentCreate, IncidentRead
from app.services.cognee_service import cognee_service


class IncidentService:
    async def create_incident(self, payload: IncidentCreate, tenant_id: UUID) -> IncidentRead:
        """Ingest a new incident write-up into memory.

        STUB (Day 1): should resolve `tenant_id` -> Cognee dataset name,
        persist incident metadata in our own DB (db/models.py), write an
        AuditLog entry, then call `cognee_service.add_incident` +
        `cognee_service.cognify`.
        """
        raise NotImplementedError

    async def get_incident(self, incident_id: UUID, tenant_id: UUID) -> IncidentRead:
        """STUB (Day 1): look up incident metadata from our own DB."""
        raise NotImplementedError

    async def list_incidents(self, tenant_id: UUID) -> list[IncidentRead]:
        """STUB (Day 1): list incidents for a tenant from our own DB."""
        raise NotImplementedError


incident_service = IncidentService()
