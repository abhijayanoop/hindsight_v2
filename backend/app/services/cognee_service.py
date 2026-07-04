"""The single boundary between Hindsight and the Cognee library.

Nothing else in this app should `import cognee`. If a route needs new
Cognee functionality, add a method to `CogneeService` here rather than
reaching into the library elsewhere — that's what keeps a Cognee version
bump (or a swap to a different memory backend) a one-file change.

Verified against cognee==1.2.2's actual API surface (both the classic
add/cognify/search/memify/prune functions and the newer
remember/recall/forget/improve surface exist in this version; we use the
classic surface below since it maps directly onto the ontology in
design/hindsight_ontology.owl — incidents are added, cognified into a
graph, queried, and durable rules are memify'd out of repeated patterns).
"""

import logging
from typing import Any
from uuid import UUID

import cognee
from cognee.modules.users.methods import get_default_user
from cognee.modules.users.models.User import User

from app.config import get_settings

logger = logging.getLogger(__name__)

_configured = False


def _configure() -> None:
    """Apply our Settings to Cognee's global config.

    Idempotent and lazy — importing this module has no side effects, and
    repeated calls (e.g. across requests) are cheap no-ops after the first.
    """
    global _configured
    if _configured:
        return

    settings = get_settings()

    cognee.config.set_llm_provider(settings.cognee_llm_provider)
    cognee.config.set_llm_model(settings.cognee_llm_model)
    if settings.cognee_llm_api_key:
        cognee.config.set_llm_api_key(settings.cognee_llm_api_key)
    if settings.cognee_llm_endpoint:
        cognee.config.set_llm_endpoint(settings.cognee_llm_endpoint)

    cognee.config.set_embedding_provider(settings.cognee_embedding_provider)
    cognee.config.set_embedding_model(settings.cognee_embedding_model)
    if settings.cognee_embedding_api_key:
        cognee.config.set_embedding_api_key(settings.cognee_embedding_api_key)

    cognee.config.set_vector_db_provider(settings.cognee_vector_db_provider)
    cognee.config.set_graph_database_provider(settings.cognee_graph_db_provider)

    cognee.config.system_root_directory(settings.cognee_system_root_directory)
    cognee.config.data_root_directory(settings.cognee_data_root_directory)

    logger.info(
        "cognee configured",
        extra={
            "llm_provider": settings.cognee_llm_provider,
            "vector_db_provider": settings.cognee_vector_db_provider,
            "graph_db_provider": settings.cognee_graph_db_provider,
        },
    )
    _configured = True


async def _get_cognee_user() -> User:
    # STUB (Day 1): once auth_service.py / dependencies.py implement real
    # auth, map the authenticated Hindsight user (and their tenant) to a
    # Cognee user + dataset instead of always using Cognee's default user.
    # Tenant isolation should ultimately come from `dataset` scoping below,
    # not from a shared default user.
    return await get_default_user()


def _dataset_for(dataset: str | None) -> str:
    return dataset or get_settings().cognee_default_dataset


class CogneeService:
    """All incident-memory operations, backed by Cognee."""

    async def add_incident(
        self,
        text: str,
        dataset: str | None = None,
        node_set: list[str] | None = None,
    ) -> None:
        """Ingest a raw incident write-up into `dataset`.

        Does not build the graph by itself — call `cognify` afterwards
        (typically batched, not per-incident) to extract entities/relations.
        """
        _configure()
        user = await _get_cognee_user()
        await cognee.add(
            text,
            dataset_name=_dataset_for(dataset),
            user=user,
            node_set=node_set,
        )

    async def cognify(self, dataset: str | None = None, temporal: bool = True) -> None:
        """Extract entities/relations and build the knowledge graph for `dataset`.

        `temporal=True` enables Cognee's temporal_cognify so incident dates
        establish an ordering the graph can reason over (e.g. recurrence).
        """
        _configure()
        user = await _get_cognee_user()
        await cognee.cognify(
            datasets=_dataset_for(dataset),
            user=user,
            temporal_cognify=temporal,
        )

    async def recall(
        self,
        query: str,
        dataset: str | None = None,
        search_type: str = "GRAPH_COMPLETION",
        top_k: int = 15,
    ) -> list[Any]:
        """Query incident memory. `search_type` must name a `cognee.SearchType` member."""
        _configure()
        user = await _get_cognee_user()
        query_type = cognee.SearchType[search_type]
        return await cognee.search(
            query_text=query,
            query_type=query_type,
            datasets=[_dataset_for(dataset)],
            top_k=top_k,
            user=user,
        )

    async def memify(self, dataset: str | None = None) -> None:
        """Derive durable PreventionRules from repeated incident patterns."""
        _configure()
        user = await _get_cognee_user()
        await cognee.memify(dataset=_dataset_for(dataset), user=user)

    async def forget(
        self,
        dataset: str | None = None,
        data_id: UUID | None = None,
        everything: bool = False,
    ) -> dict:
        """Retract a fact or ingested item (belief revision), or wipe a dataset.

        Used for the "misattributed cause" correction flow: retract the
        wrong fact so dependent graph reasoning updates.
        """
        _configure()
        user = await _get_cognee_user()
        return await cognee.forget(
            data_id=data_id,
            dataset=None if everything else _dataset_for(dataset),
            everything=everything,
            user=user,
        )

    async def get_graph(self, dataset: str | None = None) -> Any:
        """Return the knowledge graph for visualization/inspection."""
        _configure()
        return await cognee.visualize_graph()

    async def reset(self) -> None:
        """Admin-only: wipe all Cognee graph/vector/cache state."""
        _configure()
        await cognee.prune.prune_data()
        await cognee.prune.prune_system(graph=True, vector=True, metadata=False, cache=True)


cognee_service = CogneeService()
