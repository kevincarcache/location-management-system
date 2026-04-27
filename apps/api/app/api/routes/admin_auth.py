from logging import getLogger

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
logger = getLogger(__name__)


@router.post("/login", response_model=TokenPair)
async def login(payload: LoginRequest, db: Session = Depends(get_db)) -> TokenPair:
    admin = get_admin_user_by_email(db, payload.email)
    if admin is None or not verify_password(payload.password, admin.hashed_password):
        logger.warning("admin_login_failed email=%s", payload.email)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    logger.info("admin_login_success email=%s", admin.email)
    return TokenPair(
        access_token=create_access_token(subject=admin.email),
        refresh_token=create_refresh_token(subject=admin.email),
    )


@router.post("/refresh", response_model=TokenPair)
async def refresh(payload: RefreshRequest, db: Session = Depends(get_db)) -> TokenPair:
    try:
        claims = decode_token(payload.refresh_token)
    except Exception as exc:  # pragma: no cover - exact JWT exceptions depend on lib internals
        logger.warning("admin_refresh_failed reason=decode_error")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        ) from exc

    if claims.get("type") != "refresh" or not claims.get("sub"):
        logger.warning("admin_refresh_failed reason=invalid_claims")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    admin = get_admin_user_by_email(db, claims["sub"])
    if admin is None:
        logger.warning("admin_refresh_failed reason=admin_not_found email=%s", claims["sub"])
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Admin user not found")

    logger.info("admin_refresh_success email=%s", admin.email)
    return TokenPair(
        access_token=create_access_token(subject=admin.email),
        refresh_token=create_refresh_token(subject=admin.email),
    )
