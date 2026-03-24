from urllib.parse import urlencode
from urllib.request import Request, urlopen

from app.schemas.geocoding import GeocodingResultRead


def search_locations(query: str) -> list[GeocodingResultRead]:
    if not query.strip():
        return []

    params = urlencode(
        {
            "q": query.strip(),
            "format": "jsonv2",
            "limit": 5,
        }
    )
    request = Request(
        f"https://nominatim.openstreetmap.org/search?{params}",
        headers={"User-Agent": "location-management-system/0.1"},
    )

    with urlopen(request, timeout=10) as response:
        payload = response.read().decode("utf-8")

    import json

    data = json.loads(payload)
    return [
        GeocodingResultRead(
            display_name=item["display_name"],
            latitude=float(item["lat"]),
            longitude=float(item["lon"]),
        )
        for item in data
    ]
