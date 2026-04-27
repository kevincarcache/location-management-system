from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.session import Base
from app.models import Location
from app.services.locations import ensure_seed_locations


def build_session() -> Session:
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        future=True,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
    return testing_session()


def test_seed_locations_cover_each_business_type_and_are_idempotent() -> None:
    db = build_session()
    try:
        ensure_seed_locations(db)
        ensure_seed_locations(db)

        locations = list(db.scalars(select(Location)).all())
        slugs = [location.slug for location in locations]
        assert len(slugs) == len(set(slugs))

        for business_type in [
            "virtual-store",
            "nearby-event",
            "recycling-point",
            "academy",
            "technical-service",
        ]:
            active_locations = [
                location
                for location in locations
                if location.business_type == business_type and location.status == "active"
            ]
            assert len(active_locations) >= 5
    finally:
        db.close()
