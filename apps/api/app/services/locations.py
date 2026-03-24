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
        LocationCreate(
            slug="tech-lab-el-cangrejo",
            name="Tech Lab El Cangrejo",
            business_type="technical-service",
            status="active",
            description_short="Diagnóstico, reparación y soporte técnico especializado.",
            description_long=(
                "Centro técnico para laptops, móviles y equipos de punto de venta con "
                "atención el mismo día."
            ),
            address_line_1="Via Argentina, Plaza Central",
            address_line_2="Local 12B",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9852,
            longitude=-79.5318,
            phone="+507 300-3000",
            email="cangrejo@example.com",
            website="https://example.com/tech-lab",
            opening_hours={"mon-fri": ["09:00-19:00"], "sat": ["10:00-15:00"]},
            services=["repairs", "diagnostics", "onsite-support"],
            featured=True,
            external_id="seed-003",
        ),
        LocationCreate(
            slug="academy-san-francisco",
            name="Academy San Francisco",
            business_type="academy",
            status="active",
            description_short="Centro de formación con cursos cortos y bootcamps intensivos.",
            description_long=(
                "Oferta académica enfocada en habilidades digitales, operaciones y "
                "capacitación para equipos comerciales."
            ),
            address_line_1="Calle 74 Este",
            address_line_2="Edificio Nova, Nivel 2",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9946,
            longitude=-79.5061,
            phone="+507 300-4000",
            email="academy@example.com",
            website="https://example.com/academy",
            opening_hours={"mon-fri": ["08:30-18:30"]},
            services=["bootcamps", "corporate-training"],
            featured=False,
            external_id="seed-004",
        ),
        LocationCreate(
            slug="innovation-weekend-marbella",
            name="Innovation Weekend Marbella",
            business_type="nearby-event",
            status="active",
            description_short="Evento cercano con talleres, networking y experiencias de marca.",
            description_long=(
                "Encuentro temporal para lanzamiento de productos y activaciones en sitio "
                "con agenda de speakers invitados."
            ),
            address_line_1="Calle 53 Este, Centro de Convenciones",
            address_line_2="Salon Principal",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9797,
            longitude=-79.523,
            phone="+507 300-5000",
            email="events@example.com",
            website="https://example.com/events",
            opening_hours={"fri-sun": ["10:00-20:00"]},
            services=["registration", "networking"],
            featured=True,
            external_id="seed-005",
        ),
        LocationCreate(
            slug="future-opening-brisas",
            name="Future Opening Brisas",
            business_type="virtual-store",
            status="draft",
            description_short="Próxima apertura para cobertura en el corredor norte.",
            description_long="Ubicación futura reservada para expansión comercial.",
            address_line_1="Avenida Principal de Brisas del Golf",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=9.0512,
            longitude=-79.4891,
            phone="+507 300-6000",
            email="future@example.com",
            website="https://example.com/future",
            opening_hours={},
            services=["coming-soon"],
            featured=False,
            external_id="seed-006",
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
