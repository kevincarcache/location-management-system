from collections.abc import Generator
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.security import create_access_token
from app.db.session import Base, get_db
from app.main import app
from app.schemas.location import LocationCreate
from app.schemas.store_config import StoreConfigCreate
from app.services.locations import create_location
from app.services.seed import ensure_seed_admin_user
from app.services.store_configs import create_store_config


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
    ensure_seed_admin_user(db)

    def override_get_db() -> Generator[Session, None, None]:
        yield db

    app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(app), db
    finally:
        app.dependency_overrides.clear()
        db.close()


def test_admin_routes_require_access_token() -> None:
    with build_client() as (client, _):
        routes = [
            ("/api/admin/locations", 401),
            ("/api/admin/store-configs", 401),
            ("/api/admin/imports/locations/csv/template", 401),
            ("/api/admin/geocoding/search?query=panama", 401),
        ]

        for path, expected in routes:
            response = client.get(path)
            assert response.status_code == expected


def test_admin_routes_reject_invalid_token() -> None:
    with build_client() as (client, _):
        response = client.get(
            "/api/admin/locations",
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401


def test_admin_routes_accept_valid_access_token() -> None:
    with build_client() as (client, db):
        create_store_config(
            db,
            StoreConfigCreate(
                slug="default",
                brand_name="Panama Service Network",
                business_description="Red comercial de prueba.",
                theme_preset="serious-teal",
                business_type="virtual-store",
                logo_url=None,
                hero_title="Encuentra la sucursal ideal",
                hero_subtitle="Cobertura activa en Panama.",
                menu_label="Sucursales",
                footer_text="Texto de prueba.",
            ),
        )
        create_location(
            db,
            LocationCreate(
                slug="authz-location",
                name="Authorized Location",
                business_type="virtual-store",
                status="active",
                address_line_1="Avenida Central",
                city="Panama City",
                country="Panama",
                latitude=8.98,
                longitude=-79.52,
            ),
        )

        token = create_access_token("admin@example.com")
        response = client.get(
            "/api/admin/locations",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()[0]["slug"] == "authz-location"
