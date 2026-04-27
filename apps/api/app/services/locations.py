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
            slug="sucursal-albrook-mall",
            name="Sucursal Albrook Mall",
            business_type="virtual-store",
            status="active",
            description_short="Punto de atención para compras, retiros y cambios rápidos.",
            description_long=(
                "Sucursal de alto tráfico enfocada en atención comercial y soporte posventa."
            ),
            address_line_1="Pasillo del Koala, Albrook Mall",
            address_line_2="Local K-24",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9733,
            longitude=-79.5547,
            phone="+507 300-1100",
            email="albrook@example.com",
            website="https://example.com/albrook",
            opening_hours={"mon-sun": ["10:00-20:00"]},
            services=["pickup", "returns", "sales"],
            featured=True,
            external_id="seed-007",
        ),
        LocationCreate(
            slug="sucursal-altaplaza",
            name="Sucursal Altaplaza",
            business_type="virtual-store",
            status="active",
            description_short="Atención comercial y asesoría personalizada en el corredor norte.",
            description_long=(
                "Punto de servicio para clientes que buscan compras asistidas y retiros."
            ),
            address_line_1="Via Centenario, Altaplaza Mall",
            address_line_2="Nivel 2",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=9.0315,
            longitude=-79.5349,
            phone="+507 300-1200",
            email="altaplaza@example.com",
            website="https://example.com/altaplaza",
            opening_hours={"mon-sat": ["10:00-19:00"], "sun": ["11:00-18:00"]},
            services=["pickup", "consulting"],
            featured=False,
            external_id="seed-008",
        ),
        LocationCreate(
            slug="sucursal-metromall",
            name="Sucursal Metromall",
            business_type="virtual-store",
            status="active",
            description_short="Cobertura este para compras, entregas y servicio al cliente.",
            description_long=(
                "Sucursal orientada a resolver solicitudes comerciales y entregas programadas."
            ),
            address_line_1="Avenida Domingo Diaz, Metromall",
            address_line_2="Local 156",
            city="San Miguelito",
            region="Panama",
            country="Panama",
            postal_code="0701",
            latitude=9.0494,
            longitude=-79.4511,
            phone="+507 300-1300",
            email="metromall@example.com",
            website="https://example.com/metromall",
            opening_hours={"mon-sun": ["10:00-20:00"]},
            services=["pickup", "support"],
            featured=False,
            external_id="seed-009",
        ),
        LocationCreate(
            slug="sucursal-david-centro",
            name="Sucursal David Centro",
            business_type="virtual-store",
            status="active",
            description_short="Sucursal regional para atencion comercial en Chiriqui.",
            description_long="Centro de cobertura regional para clientes del occidente del pais.",
            address_line_1="Avenida Central, Plaza Terronal",
            city="David",
            region="Chiriqui",
            country="Panama",
            postal_code="0401",
            latitude=8.4273,
            longitude=-82.4309,
            phone="+507 300-1400",
            email="david@example.com",
            website="https://example.com/david",
            opening_hours={"mon-fri": ["08:30-18:00"], "sat": ["09:00-14:00"]},
            services=["sales", "pickup", "regional-support"],
            featured=True,
            external_id="seed-010",
        ),
        LocationCreate(
            slug="punto-verde-condado",
            name="Punto Verde Condado del Rey",
            business_type="recycling-point",
            status="active",
            description_short="Recepcion de papel, vidrio, plastico y empaques limpios.",
            description_long="Punto comunitario para acopio responsable y charlas de separacion.",
            address_line_1="Avenida Condado del Rey",
            address_line_2="Plaza 88",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=9.0285,
            longitude=-79.5306,
            phone="+507 300-2100",
            email="condadoverde@example.com",
            website="https://example.com/condado-verde",
            opening_hours={"mon-sat": ["08:00-17:00"]},
            services=["recycling", "sorting-guidance"],
            featured=True,
            external_id="seed-011",
        ),
        LocationCreate(
            slug="punto-verde-obarrio",
            name="Punto Verde Obarrio",
            business_type="recycling-point",
            status="active",
            description_short="Acopio urbano para reciclaje de oficina y residuos domesticos.",
            description_long=(
                "Centro compacto con horarios extendidos para empresas y residentes cercanos."
            ),
            address_line_1="Calle 60 Este, Obarrio",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9869,
            longitude=-79.5191,
            phone="+507 300-2200",
            email="obarriorecicla@example.com",
            website="https://example.com/obarrio-recicla",
            opening_hours={"mon-fri": ["07:00-18:00"], "sat": ["08:00-13:00"]},
            services=["recycling", "corporate-pickup"],
            featured=False,
            external_id="seed-012",
        ),
        LocationCreate(
            slug="punto-verde-clayton",
            name="Punto Verde Clayton",
            business_type="recycling-point",
            status="active",
            description_short="Centro de acopio para comunidades residenciales y educativas.",
            description_long=(
                "Punto de reciclaje con enfasis en jornadas familiares y clasificacion guiada."
            ),
            address_line_1="Ciudad del Saber, Edificio 105",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0843",
            latitude=8.9997,
            longitude=-79.5821,
            phone="+507 300-2300",
            email="claytonverde@example.com",
            website="https://example.com/clayton-verde",
            opening_hours={"mon-sat": ["08:00-16:00"]},
            services=["recycling", "education", "community-events"],
            featured=False,
            external_id="seed-013",
        ),
        LocationCreate(
            slug="punto-verde-la-chorrera",
            name="Punto Verde La Chorrera",
            business_type="recycling-point",
            status="active",
            description_short="Cobertura oeste para reciclaje residencial y comercial.",
            description_long=(
                "Centro regional de acopio para materiales limpios y pequenas empresas."
            ),
            address_line_1="Avenida de Las Americas",
            city="La Chorrera",
            region="Panama Oeste",
            country="Panama",
            postal_code="1001",
            latitude=8.8812,
            longitude=-79.7836,
            phone="+507 300-2400",
            email="chorreraverde@example.com",
            website="https://example.com/chorrera-verde",
            opening_hours={"mon-fri": ["08:00-17:00"], "sat": ["08:00-12:00"]},
            services=["recycling", "bulk-dropoff"],
            featured=True,
            external_id="seed-014",
        ),
        LocationCreate(
            slug="tech-lab-costa-del-este",
            name="Tech Lab Costa del Este",
            business_type="technical-service",
            status="active",
            description_short="Soporte tecnico para equipos empresariales y dispositivos moviles.",
            description_long=(
                "Laboratorio orientado a diagnostico rapido y soporte para equipos de trabajo."
            ),
            address_line_1="Avenida Centenario, PH Prime Time",
            address_line_2="Local 3",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=9.0094,
            longitude=-79.4733,
            phone="+507 300-3100",
            email="costadeleste-tech@example.com",
            website="https://example.com/tech-cde",
            opening_hours={"mon-fri": ["08:30-18:30"], "sat": ["09:00-14:00"]},
            services=["repairs", "diagnostics", "business-support"],
            featured=True,
            external_id="seed-015",
        ),
        LocationCreate(
            slug="tech-lab-brisas",
            name="Tech Lab Brisas del Golf",
            business_type="technical-service",
            status="active",
            description_short="Reparaciones, mantenimiento y configuracion de equipos.",
            description_long="Centro tecnico para hogares y pequenos negocios del corredor norte.",
            address_line_1="Avenida Brisas del Golf",
            address_line_2="Plaza Village",
            city="San Miguelito",
            region="Panama",
            country="Panama",
            postal_code="0701",
            latitude=9.0526,
            longitude=-79.4917,
            phone="+507 300-3200",
            email="brisas-tech@example.com",
            website="https://example.com/tech-brisas",
            opening_hours={"mon-fri": ["09:00-18:00"], "sat": ["09:00-13:00"]},
            services=["repairs", "maintenance"],
            featured=False,
            external_id="seed-016",
        ),
        LocationCreate(
            slug="tech-lab-los-pueblos",
            name="Tech Lab Los Pueblos",
            business_type="technical-service",
            status="active",
            description_short="Soporte tecnico express para el area este.",
            description_long=(
                "Punto tecnico con atencion por cita y reparaciones de prioridad media."
            ),
            address_line_1="Centro Comercial Los Pueblos",
            address_line_2="Local B-18",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=9.0545,
            longitude=-79.4563,
            phone="+507 300-3300",
            email="lospueblos-tech@example.com",
            website="https://example.com/tech-los-pueblos",
            opening_hours={"mon-sat": ["10:00-18:00"]},
            services=["diagnostics", "repairs", "device-setup"],
            featured=False,
            external_id="seed-017",
        ),
        LocationCreate(
            slug="tech-lab-santiago",
            name="Tech Lab Santiago",
            business_type="technical-service",
            status="active",
            description_short="Centro regional para soporte tecnico en Veraguas.",
            description_long=(
                "Laboratorio regional para diagnostico, reparacion y atencion programada."
            ),
            address_line_1="Avenida Central, Plaza Banconal",
            city="Santiago",
            region="Veraguas",
            country="Panama",
            postal_code="0901",
            latitude=8.1004,
            longitude=-80.9834,
            phone="+507 300-3400",
            email="santiago-tech@example.com",
            website="https://example.com/tech-santiago",
            opening_hours={"mon-fri": ["08:30-17:30"], "sat": ["09:00-12:00"]},
            services=["repairs", "diagnostics", "regional-support"],
            featured=True,
            external_id="seed-018",
        ),
        LocationCreate(
            slug="academy-bella-vista",
            name="Academy Bella Vista",
            business_type="academy",
            status="active",
            description_short="Cursos cortos para equipos comerciales y operadores.",
            description_long=(
                "Centro academico para capacitaciones presenciales y talleres intensivos."
            ),
            address_line_1="Calle 45 Este, Bella Vista",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9821,
            longitude=-79.5257,
            phone="+507 300-4100",
            email="bellavista-academy@example.com",
            website="https://example.com/academy-bella-vista",
            opening_hours={"mon-fri": ["08:00-19:00"]},
            services=["workshops", "corporate-training"],
            featured=True,
            external_id="seed-019",
        ),
        LocationCreate(
            slug="academy-clayton",
            name="Academy Clayton",
            business_type="academy",
            status="active",
            description_short="Formacion practica para tecnologia, operaciones y servicio.",
            description_long=(
                "Sede academica con aulas flexibles y laboratorios para equipos de trabajo."
            ),
            address_line_1="Ciudad del Saber, Calle Gustavo Lara",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0843",
            latitude=9.0009,
            longitude=-79.5862,
            phone="+507 300-4200",
            email="clayton-academy@example.com",
            website="https://example.com/academy-clayton",
            opening_hours={"mon-sat": ["08:30-17:30"]},
            services=["bootcamps", "labs", "team-training"],
            featured=False,
            external_id="seed-020",
        ),
        LocationCreate(
            slug="academy-colon",
            name="Academy Colon",
            business_type="academy",
            status="active",
            description_short="Capacitaciones regionales para equipos del Atlantico.",
            description_long=(
                "Sede regional para cursos de servicio, operaciones y habilidades digitales."
            ),
            address_line_1="Calle 11, Zona Libre",
            city="Colon",
            region="Colon",
            country="Panama",
            postal_code="0301",
            latitude=9.3592,
            longitude=-79.9005,
            phone="+507 300-4300",
            email="colon-academy@example.com",
            website="https://example.com/academy-colon",
            opening_hours={"mon-fri": ["08:00-17:00"]},
            services=["training", "certifications"],
            featured=False,
            external_id="seed-021",
        ),
        LocationCreate(
            slug="academy-penonome",
            name="Academy Penonome",
            business_type="academy",
            status="active",
            description_short="Centro de aprendizaje para habilidades operativas y digitales.",
            description_long=(
                "Aulas para talleres regionales, entrenamiento comercial y programas intensivos."
            ),
            address_line_1="Avenida Juan Demostenes Arosemena",
            city="Penonome",
            region="Cocle",
            country="Panama",
            postal_code="0201",
            latitude=8.5189,
            longitude=-80.3573,
            phone="+507 300-4400",
            email="penonome-academy@example.com",
            website="https://example.com/academy-penonome",
            opening_hours={"mon-fri": ["08:30-17:30"], "sat": ["09:00-13:00"]},
            services=["workshops", "regional-training"],
            featured=True,
            external_id="seed-022",
        ),
        LocationCreate(
            slug="festival-tech-casco",
            name="Festival Tech Casco",
            business_type="nearby-event",
            status="active",
            description_short="Evento de tecnologia, demostraciones y networking en Casco Antiguo.",
            description_long=(
                "Activacion temporal con experiencias de producto y sesiones para comunidades."
            ),
            address_line_1="Plaza Herrera, Casco Antiguo",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9515,
            longitude=-79.5355,
            phone="+507 300-5100",
            email="festivaltech@example.com",
            website="https://example.com/festival-tech",
            opening_hours={"fri-sun": ["11:00-21:00"]},
            services=["registration", "demos", "networking"],
            featured=True,
            external_id="seed-023",
        ),
        LocationCreate(
            slug="expo-sostenible-amador",
            name="Expo Sostenible Amador",
            business_type="nearby-event",
            status="active",
            description_short=(
                "Feria de sostenibilidad con stands, charlas y experiencias familiares."
            ),
            description_long=(
                "Evento cercano para iniciativas verdes, reciclaje y proyectos comunitarios."
            ),
            address_line_1="Centro de Convenciones Amador",
            city="Panama City",
            region="Panama",
            country="Panama",
            postal_code="0801",
            latitude=8.9347,
            longitude=-79.5457,
            phone="+507 300-5200",
            email="expoamador@example.com",
            website="https://example.com/expo-amador",
            opening_hours={"sat-sun": ["10:00-19:00"]},
            services=["registration", "workshops", "community"],
            featured=False,
            external_id="seed-024",
        ),
        LocationCreate(
            slug="summit-operaciones-tocumen",
            name="Summit Operaciones Tocumen",
            business_type="nearby-event",
            status="active",
            description_short=(
                "Encuentro para equipos logisticos, soporte y operaciones regionales."
            ),
            description_long=(
                "Evento temporal con charlas de mejora operativa y demostraciones de servicio."
            ),
            address_line_1="Hotel Riande Aeropuerto",
            city="Tocumen",
            region="Panama",
            country="Panama",
            postal_code="0819",
            latitude=9.0558,
            longitude=-79.3836,
            phone="+507 300-5300",
            email="summitops@example.com",
            website="https://example.com/summit-ops",
            opening_hours={"thu-fri": ["09:00-18:00"]},
            services=["registration", "talks", "operations-lab"],
            featured=False,
            external_id="seed-025",
        ),
        LocationCreate(
            slug="marketplace-day-boquete",
            name="Marketplace Day Boquete",
            business_type="nearby-event",
            status="active",
            description_short=(
                "Evento regional para comercios, emprendimientos y experiencias de marca."
            ),
            description_long=(
                "Jornada temporal con networking, demostraciones y vitrinas comerciales."
            ),
            address_line_1="Parque Central de Boquete",
            city="Boquete",
            region="Chiriqui",
            country="Panama",
            postal_code="0413",
            latitude=8.7803,
            longitude=-82.4409,
            phone="+507 300-5400",
            email="boquete-market@example.com",
            website="https://example.com/boquete-market",
            opening_hours={"sat": ["09:00-18:00"], "sun": ["10:00-15:00"]},
            services=["registration", "marketplace", "networking"],
            featured=True,
            external_id="seed-026",
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
    db.commit()


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
    db.commit()
    db.refresh(location)
    return _serialize_location(location)


def get_location(db: Session, location_id: str) -> LocationRead | None:
    location = get_location_by_id(db, location_id)
    if location is None:
        return None
    return _serialize_location(location)


def update_location(db: Session, location_id: str, payload: LocationUpdate) -> LocationRead | None:
    location = get_location_by_id(db, location_id)
    if location is None:
        return None
    updated = update_location_record(db, location, payload)
    db.commit()
    db.refresh(updated)
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
    db.commit()
    return True
