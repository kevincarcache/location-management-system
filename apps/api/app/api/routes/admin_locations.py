from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user
from app.db.session import get_db
from app.schemas.location import LocationCreate, LocationRead, LocationUpdate
from app.services.locations import (
    create_location,
    delete_location,
    get_location,
    list_locations,
    update_location,
)

router = APIRouter(dependencies=[Depends(get_current_admin_user)])


@router.get("", response_model=list[LocationRead])
async def get_locations(db: Session = Depends(get_db)) -> list[LocationRead]:
    return list_locations(db)


@router.get("/{location_id}", response_model=LocationRead)
async def get_location_detail(location_id: str, db: Session = Depends(get_db)) -> LocationRead:
    location = get_location(db, location_id)
    if location is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location


@router.post("", response_model=LocationRead, status_code=201)
async def post_location(payload: LocationCreate, db: Session = Depends(get_db)) -> LocationRead:
    return create_location(db, payload)


@router.patch("/{location_id}", response_model=LocationRead)
async def patch_location(
    location_id: str,
    payload: LocationUpdate,
    db: Session = Depends(get_db),
) -> LocationRead:
    updated = update_location(db, location_id, payload)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return updated


@router.delete("/{location_id}", status_code=204)
async def remove_location(location_id: str, db: Session = Depends(get_db)) -> None:
    deleted = delete_location(db, location_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
