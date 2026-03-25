import json
from dataclasses import dataclass
from urllib.parse import urlencode
from urllib.request import Request, urlopen


@dataclass(slots=True)
class GeocodingResult:
    display_name: str
    latitude: float
    longitude: float


class GeocodingProvider:
    def search(self, query: str) -> list[GeocodingResult]:
        raise NotImplementedError


@dataclass(slots=True)
class NominatimGeocodingProvider(GeocodingProvider):
    base_url: str
    user_agent: str
    timeout_seconds: int
    limit: int

    def search(self, query: str) -> list[GeocodingResult]:
        params = urlencode(
            {
                "q": query.strip(),
                "format": "jsonv2",
                "limit": self.limit,
            }
        )
        request = Request(
            f"{self.base_url}?{params}",
            headers={"User-Agent": self.user_agent},
        )

        with urlopen(request, timeout=self.timeout_seconds) as response:
            payload = response.read().decode("utf-8")

        data = json.loads(payload)
        return [
            GeocodingResult(
                display_name=item["display_name"],
                latitude=float(item["lat"]),
                longitude=float(item["lon"]),
            )
            for item in data
        ]
