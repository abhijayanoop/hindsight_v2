"""User/role/tenant business logic.

STUB: `db/models.py` (User, Role, Tenant) is defined and ready, and
`core/security.py` has working password hashing + JWT primitives, but the
logic that ties them together (registration, login, role checks) is not
implemented yet. This is intentionally left for Day 1.
"""

from uuid import UUID

from app.db.models import User
from app.schemas.auth import UserCreate


class AuthService:
    async def authenticate(self, email: str, password: str) -> User:
        """STUB (Day 1): look up user by email, verify password via
        `core.security.verify_password`, return the User or raise."""
        raise NotImplementedError

    async def register_user(self, payload: UserCreate) -> User:
        """STUB (Day 1): create tenant (if needed) + user row, hash password
        via `core.security.hash_password`."""
        raise NotImplementedError

    async def get_user_by_id(self, user_id: UUID) -> User:
        """STUB (Day 1): fetch a user for token-subject resolution."""
        raise NotImplementedError

    async def user_has_role(self, user: User, role_name: str) -> bool:
        """STUB (Day 1): role-based access check."""
        raise NotImplementedError


auth_service = AuthService()
