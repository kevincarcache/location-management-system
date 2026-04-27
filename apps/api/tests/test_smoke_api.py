from collections.abc import Generator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base, get_db
from app.main import app
from app.services.locations import ensure_seed_locations
from app.services.seed import ensure_seed_admin_user
from app.services.store_configs import ensure_seed_store_config


@contextmanager
def build_client() -> Generator[tuple[TestClient, Session], None, None]:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
    db = testing_session()
    ensure_seed_locations(db)
    ensure_seed_store_config(db)
    ensure_seed_admin_user(db)

    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), db
    finally:
        app.dependency_overrides.clear()
        db.close()


def test_public_storefront_and_admin_import_flow_smoke() -> None:
    with build_client() as (client, _):
        health = client.get("/api/health")
        assert health.status_code == 200

        store_config = client.get("/api/public/store-config")
        assert store_config.status_code == 200
        assert store_config.json()["slug"] == "default"

        locations = client.get("/api/public/locations")
        assert locations.status_code == 200
        assert len(locations.json()) >= 1

        login = client.post(
            "/api/admin/auth/login",
            json={"email": "admin@example.com", "password": "ChangeMe123!"},
        )
        assert login.status_code == 200
        tokens = login.json()

        preview_csv = "\n".join(
            [
                "external_id,slug,name,business_type,address_line_1,city,country,latitude,longitude",
                (
                    "smoke-001,smoke-location,Smoke Location,virtual-store,"
                    "Calle 50,Panama City,Panama,9.01,-79.51"
                ),
            ]
        )
        preview = client.post(
            "/api/admin/imports/locations/csv/preview",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
            files={"file": ("smoke.csv", preview_csv, "text/csv")},
        )
        assert preview.status_code == 200
        assert preview.json()["create_candidates"] == 1

        upload = client.post(
            "/api/admin/imports/locations/csv",
            headers={"Authorization": f"Bearer {tokens['access_token']}"},
            files={"file": ("smoke.csv", preview_csv, "text/csv")},
        )
        assert upload.status_code == 202
        job = upload.json()
        assert job["created"] == 1
        assert job["rejected"] == 0

        imported_location = client.get("/api/public/locations/smoke-location")
        assert imported_location.status_code == 200
        assert imported_location.json()["name"] == "Smoke Location"
