"""Shared FastAPI dependencies.

Auth dependencies are stubs: they establish the shape every router will
depend on (`get_current_user`, `require_role`) so routes can be wired up
today, but they don't actually validate anything yet. Replace the bodies
once `services/auth_service.py` is implemented — no router should need to
change when that happens.
"""

from collections.abc import AsyncGenerator
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async for session in get_db_session():
        yield session


class CurrentUser:
    """Placeholder shape for the authenticated principal.

    STUB (Day 1): replace with the real `db.models.User` once
    `get_current_user` below decodes and validates tokens.
    """

    def __init__(self, id: UUID, tenant_id: UUID, email: str, roles: list[str]):
        self.id = id
        self.tenant_id = tenant_id
        self.email = email
        self.roles = roles


async def get_current_user(
    token: str | None = Depends(oauth2_scheme),
) -> CurrentUser:
    """STUB (Day 1): decode `token` via `core.security.decode_access_token`,
    load the user via `services.auth_service.get_user_by_id`, and return it.

    Currently raises 501 so protected routes fail loudly and visibly
    instead of silently admitting unauthenticated requests.
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Authentication is not implemented yet.",
    )


def require_role(role_name: str):
    """STUB (Day 1): dependency factory for role-gated routes, e.g.
    `Depends(require_role("admin"))`. Wire up to
    `services.auth_service.user_has_role` once auth lands.
    """

    async def _check(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED,
            detail=f"Role check for '{role_name}' is not implemented yet.",
        )

    return _check
