from logging import getLogger

from app.core.config import settings
from app.schemas.geocoding import GeocodingResultRead
from app.services.geocoding_provider import (
    GeocodingProvider,
    NominatimGeocodingProvider,
)

logger = getLogger(__name__)


def _build_provider() -> GeocodingProvider:
    return NominatimGeocodingProvider(
        base_url=settings.geocoding_base_url,
        user_agent=settings.geocoding_user_agent,
        timeout_seconds=settings.geocoding_timeout_seconds,
        limit=settings.geocoding_limit,
    )


def search_locations(
    query: str,
    provider: GeocodingProvider | None = None,
) -> list[GeocodingResultRead]:
    if not query.strip():
        return []

    geocoding_provider = provider or _build_provider()
    logger.info("geocoding_search query=%s", query.strip())
    data = geocoding_provider.search(query)
    return [
        GeocodingResultRead(
            display_name=item.display_name,
            latitude=item.latitude,
            longitude=item.longitude,
        )
        for item in data
    ]
