"""Auth endpoints. STUB (Day 1): shapes are settled, logic is not.

See `services/auth_service.py` and `core/security.py`.
"""

from fastapi import APIRouter, HTTPException, status

from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate) -> UserRead:
    """STUB (Day 1): create tenant/user via `services.auth_service.register_user`."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Registration is not implemented yet.",
    )


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest) -> Token:
    """STUB (Day 1): authenticate via `services.auth_service.authenticate`
    and issue a token via `core.security.create_access_token`."""
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login is not implemented yet.",
    )
