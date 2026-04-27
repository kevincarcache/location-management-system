from app.services.geocoding import search_locations
from app.services.geocoding_provider import GeocodingProvider, GeocodingResult


class FakeGeocodingProvider(GeocodingProvider):
    def search(self, query: str) -> list[GeocodingResult]:
        return [
            GeocodingResult(
                display_name=f"Result for {query}",
                latitude=8.98,
                longitude=-79.52,
            )
        ]


def test_search_locations_uses_provider_adapter() -> None:
    results = search_locations("Panama", provider=FakeGeocodingProvider())

    assert len(results) == 1
    assert results[0].display_name == "Result for Panama"
    assert results[0].latitude == 8.98


def test_search_locations_returns_empty_for_blank_query() -> None:
    assert search_locations("   ", provider=FakeGeocodingProvider()) == []
