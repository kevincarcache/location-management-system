from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.store_config import StoreConfigRead
from app.services.store_configs import resolve_store_config

router = APIRouter()


@router.get("", response_model=StoreConfigRead)
async def get_public_store_config(
    storeview: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> StoreConfigRead:
    try:
        return resolve_store_config(db, requested_slug=storeview)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
