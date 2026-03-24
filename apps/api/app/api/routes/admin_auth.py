from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_token,
    verify_password,
)
from app.db.session import get_db
from app.repositories.admin_users import get_admin_user_by_email
from app.schemas.auth import LoginRequest, RefreshRequest, TokenPair

router = APIRouter()


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    admin = get_admin_user_by_email(db, payload.email)
    if admin is None or not verify_password(payload.password, admin.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    return TokenPair(
        access_token=create_access_token(subject=admin.email),
        refresh_token=create_refresh_token(subject=admin.email),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenPair:
    try:
        claims = decode_token(payload.refresh_token)
    except Exception as exc:  # pragma: no cover - exact JWT exceptions depend on lib internals
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from exc

    if claims.get("type") != "refresh" or not claims.get("sub"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    admin = get_admin_user_by_email(db, claims["sub"])
    if admin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")

    return TokenPair(
        access_token=create_access_token(subject=admin.email),
        refresh_token=create_refresh_token(subject=admin.email),
    )
