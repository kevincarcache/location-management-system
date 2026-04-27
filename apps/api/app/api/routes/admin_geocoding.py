from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.dependencies import get_current_admin_user
from app.schemas.geocoding import GeocodingResultRead
from app.services.geocoding import search_locations

router = APIRouter(dependencies=[Depends(get_current_admin_user)])


@router.get("/search", response_model=list[GeocodingResultRead])
async def get_geocoding_results(
    query: str = Query(..., min_length=2),
) -> list[GeocodingResultRead]:
    try:
        return search_locations(query)
    except RuntimeError as error:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        ) from error
