from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user
from app.db.session import get_db
from app.schemas.store_config import StoreConfigCreate, StoreConfigRead, StoreConfigUpdate
from app.services.store_configs import create_store_config, list_store_configs, update_store_config

router = APIRouter(dependencies=[Depends(get_current_admin_user)])


@router.get("", response_model=list[StoreConfigRead])
async def get_store_configs(db: Session = Depends(get_db)) -> list[StoreConfigRead]:
    return list_store_configs(db)


@router.post("", response_model=StoreConfigRead, status_code=201)
async def post_store_config(
    payload: StoreConfigCreate,
    db: Session = Depends(get_db),
) -> StoreConfigRead:
    return create_store_config(db, payload)


@router.patch("/{store_config_id}", response_model=StoreConfigRead)
async def patch_store_config(
    store_config_id: str,
    payload: StoreConfigUpdate,
    db: Session = Depends(get_db),
) -> StoreConfigRead:
    updated = update_store_config(db, store_config_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Store config not found")
    return updated
