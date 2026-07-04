"""Async SQLAlchemy engine/session for Hindsight's own application database.

This is deliberately separate from Cognee's storage — this DB holds our
users, roles, tenants, and audit log. Cognee manages its own graph/vector
stores entirely behind `services/cognee_service.py`.
"""

from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings


class Base(DeclarativeBase):
    """Declarative base for all ORM models in `db/models.py`."""


_settings = get_settings()

engine: AsyncEngine = create_async_engine(
    _settings.database_url,
    echo=_settings.database_echo,
    future=True,
)

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields a request-scoped DB session."""
    async with async_session_factory() as session:
        yield session


async def init_db() -> None:
    """Create tables if they don't exist.

    Fine for local dev / first boot. Production migrations should go
    through Alembic instead of relying on this.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()
