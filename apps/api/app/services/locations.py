from sqlalchemy.orm import Session

from app.models.location import Location
from app.repositories.locations import (
    create_location as create_location_record,
)
from app.repositories.locations import (
    delete_location as delete_location_record,
)
from app.repositories.locations import (
    get_location_by_id,
    get_location_by_slug,
)
from app.repositories.locations import (
    list_locations as list_location_records,
)
from app.repositories.locations import (
    update_location as update_location_record,
)
from app.schemas.location import LocationCreate, LocationRead, LocationUpdate


def _serialize_location(location: Location) -> LocationRead:
    return LocationRead.model_validate(location, from_attributes=True)


def ensure_seed_locations(db: Session) -> None:
    defaults = [
        LocationCreate(
            slug="panama-city-hub",
            name="Panama City Hub",
            business_type="virtual-store",
            status="active",
            description_short="Centro principal para retiros, asesoría y soporte.",
            description_long=(
                "Sucursal principal orientada a atención omnicanal y operaciones urbanas."
            ),
            address_line_1="Avenida Balboa, Torre Central",
            address_line_2="Piso 4",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9824,
            longitude=-79.5199,
            phone="+507 300-1000",
            email="balboa@example.com",
            website="https://example.com/balboa",
            opening_hours={"mon-fri": ["08:00-18:00"], "sat": ["09:00-13:00"]},
            services=["pickup", "consulting"],
            featured=True,
            external_id="seed-001",
        ),
        LocationCreate(
            slug="recycling-costa-del-este",
            name="Punto Verde Costa del Este",
            business_type="recycling-point",
            status="active",
            description_short="Recepción de plásticos, cartón y electrónicos.",
            description_long="Centro de reciclaje con jornadas educativas de fin de semana.",
            address_line_1="Boulevard Costa del Este",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=9.0075,
            longitude=-79.4818,
            phone="+507 300-2000",
            email="verde@example.com",
            website="https://example.com/verde",
            opening_hours={"mon-sat": ["07:30-17:30"]},
            services=["recycling", "education"],
            featured=False,
            external_id="seed-002",
        ),
    ]

    for item in defaults:
        existing = get_location_by_slug(db, item.slug)
        if existing:
            continue
        create_location_record(db, item)


def list_locations(
    db: Session,
    query: str | None = None,
    business_type: str | None = None,
    public_only: bool = False,
) -> list[LocationRead]:
    locations = list_location_records(
        db,
        query=query,
        business_type=business_type,
        public_only=public_only,
    )
    return [_serialize_location(location) for location in locations]


def create_location(db: Session, payload: LocationCreate) -> LocationRead:
    location = create_location_record(db, payload)
    return _serialize_location(location)


def update_location(db: Session, location_id: str, payload: LocationUpdate) -> LocationRead | None:
    location = get_location_by_id(db, location_id)
    if location is None:
        return None
    updated = update_location_record(db, location, payload)
    return _serialize_location(updated)


def find_location_by_slug(db: Session, slug: str) -> LocationRead | None:
    location = get_location_by_slug(db, slug, public_only=True)
    if location is None:
        return None
    return _serialize_location(location)


def delete_location(db: Session, location_id: str) -> bool:
    location = get_location_by_id(db, location_id)
    if location is None:
        return False
    delete_location_record(db, location)
    return True
