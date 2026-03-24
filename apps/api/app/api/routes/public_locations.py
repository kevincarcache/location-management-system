from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.location import LocationRead
from app.services.locations import find_location_by_slug, list_locations
from app.services.store_configs import resolve_store_config

router = APIRouter()


@router.get("", response_model=list[LocationRead])
async def get_public_locations(
    query: str | None = Query(default=None),
    business_type: str | None = Query(default=None),
    storeview: str | None = Query(default=None),
    db: Session = Depends(get_db),
) -> list[LocationRead]:
    resolved_store = resolve_store_config(db, requested_slug=storeview)
    effective_business_type = business_type or resolved_store.business_type
    return list_locations(db, query=query, business_type=effective_business_type, public_only=True)


@router.get("/{slug}", response_model=LocationRead)
async def get_public_location(slug: str, db: Session = Depends(get_db)) -> LocationRead:
    location = find_location_by_slug(db, slug)
    if not location:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Location not found")
    return location
