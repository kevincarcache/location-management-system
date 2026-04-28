from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_allows_kevincarcache_subdomain_origin() -> None:
    response = client.options(
        "/api/health",
        headers={
            "Origin": "https://admin.kevincarcache.com",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "https://admin.kevincarcache.com"


def test_rejects_similar_external_origin() -> None:
    response = client.options(
        "/api/health",
        headers={
            "Origin": "https://kevincarcache.com.evil.example",
            "Access-Control-Request-Method": "GET",
        },
    )

    assert response.status_code == 400
    assert "access-control-allow-origin" not in response.headers
