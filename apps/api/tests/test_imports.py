from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base
from app.models import Location
from app.services.imports import import_locations_csv, preview_locations_csv
from app.services.location_imports.parser import build_location_payload, read_csv_rows
from app.services.location_imports.planner import build_import_plan
from app.services.locations import ensure_seed_locations


def make_db() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
    db = testing_session()
    ensure_seed_locations(db)
    return db


def test_preview_locations_csv_reports_create_update_and_reject() -> None:
    db = make_db()
    csv_content = "\n".join(
        [
            "external_id,slug,name,business_type,address_line_1,city,country,latitude,longitude",
            (
                "seed-001,panama-city-hub,Panama City Hub,virtual-store,"
                "Avenida Balboa,Panama City,Panama,8.9824,-79.5199"
            ),
            "new-001,new-academy,Nueva Academia,academy,Calle 50,Panama City,Panama,9.01,-79.51",
            (
                "broken-001,broken-row,Broken Row,academy,Calle 50,"
                "Panama City,Panama,not-a-number,-79.50"
            ),
        ]
    ).encode("utf-8")

    preview = preview_locations_csv(db, filename="preview.csv", content=csv_content)

    assert preview.total_rows == 3
    assert preview.create_candidates == 1
    assert preview.update_candidates == 1
    assert preview.rejected_rows == 1
    assert any(row.action == "reject" for row in preview.rows)


def test_import_locations_csv_creates_updates_and_stores_errors() -> None:
    db = make_db()
    csv_content = "\n".join(
        [
            "external_id,slug,name,business_type,address_line_1,city,country,latitude,longitude",
            (
                "seed-001,panama-city-hub,Panama City Hub Updated,virtual-store,"
                "Avenida Balboa,Panama City,Panama,8.9824,-79.5199"
            ),
            "new-001,new-academy,Nueva Academia,academy,Calle 50,Panama City,Panama,9.01,-79.51",
            (
                "broken-001,broken-row,Broken Row,academy,Calle 50,"
                "Panama City,Panama,not-a-number,-79.50"
            ),
        ]
    ).encode("utf-8")

    job = import_locations_csv(db, filename="import.csv", content=csv_content)

    assert job.created == 1
    assert job.updated == 1
    assert job.rejected == 1
    assert len(job.errors) == 1

    updated_location = db.query(Location).filter(Location.slug == "panama-city-hub").one()
    created_location = db.query(Location).filter(Location.slug == "new-academy").one()

    assert updated_location.name == "Panama City Hub Updated"
    assert created_location.name == "Nueva Academia"


def test_read_csv_rows_requires_required_headers() -> None:
    db = make_db()
    del db

    csv_content = "name,city\nBroken,Panama City\n".encode("utf-8")

    try:
        read_csv_rows(csv_content)
    except ValueError as exc:
        assert "required columns" in str(exc)
    else:
        raise AssertionError("Expected read_csv_rows to reject missing headers")


def test_build_location_payload_parses_optional_fields() -> None:
    payload = build_location_payload(
        {
            "external_id": "academy-001",
            "slug": "",
            "name": "Nueva Academia / Centro",
            "business_type": "academy",
            "status": "",
            "description_short": "Test",
            "description_long": "Long test",
            "address_line_1": "Calle 50",
            "address_line_2": "Piso 2",
            "city": "Panama City",
            "region": "Panama",
            "country": "Panama",
            "postal_code": "0801",
            "latitude": "9.01",
            "longitude": "-79.51",
            "phone": "+507 300-1000",
            "email": "academy@example.com",
            "website": "https://example.com",
            "opening_hours": '{"mon":["08:00-17:00"]}',
            "services": "pickup| consulting ",
            "featured": "yes",
        }
    )

    assert payload.slug == "nueva-academia-centro"
    assert payload.status == "active"
    assert payload.opening_hours == {"mon": ["08:00-17:00"]}
    assert payload.services == ["pickup", "consulting"]
    assert payload.featured is True


def test_build_import_plan_classifies_create_update_and_reject() -> None:
    db = make_db()
    csv_content = "\n".join(
        [
            "external_id,slug,name,business_type,address_line_1,city,country,latitude,longitude",
            (
                "seed-001,panama-city-hub,Panama City Hub,virtual-store,"
                "Avenida Balboa,Panama City,Panama,8.9824,-79.5199"
            ),
            "new-001,new-academy,Nueva Academia,academy,Calle 50,Panama City,Panama,9.01,-79.51",
            (
                "broken-001,broken-row,Broken Row,academy,Calle 50,"
                "Panama City,Panama,not-a-number,-79.50"
            ),
        ]
    ).encode("utf-8")

    plans = build_import_plan(db, content=csv_content)

    assert [plan.action for plan in plans] == ["update", "create", "reject"]
