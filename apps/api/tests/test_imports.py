from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.db.session import Base
from app.models import Location
from app.services.imports import import_locations_csv, preview_locations_csv
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
