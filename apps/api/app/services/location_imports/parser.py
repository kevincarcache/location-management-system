import csv
import json
from io import StringIO

from app.schemas.location import LocationCreate
from app.services.location_imports.models import (
    REQUIRED_COLUMNS,
    TEMPLATE_HEADERS,
    ParsedImportRow,
)


def read_csv_rows(content: bytes) -> list[ParsedImportRow]:
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(StringIO(decoded))

    if not reader.fieldnames:
        raise ValueError("CSV file is missing a header row")

    missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

    return [
        ParsedImportRow(row_number=row_number, raw=row)
        for row_number, row in enumerate(reader, start=2)
    ]


def build_location_payload(row: dict[str, str]) -> LocationCreate:
    return LocationCreate(
        slug=row.get("slug") or _slugify(row["name"]),
        name=row["name"],
        business_type=row["business_type"],
        status=row.get("status") or "active",
        description_short=row.get("description_short"),
        description_long=row.get("description_long"),
        address_line_1=row["address_line_1"],
        address_line_2=row.get("address_line_2"),
        city=row["city"],
        region=row.get("region"),
        country=row["country"],
        postal_code=row.get("postal_code"),
        latitude=float(row["latitude"]),
        longitude=float(row["longitude"]),
        phone=row.get("phone"),
        email=row.get("email"),
        website=row.get("website"),
        opening_hours=_parse_json_field(row.get("opening_hours"), default={}),
        services=_parse_list_field(row.get("services")),
        featured=_parse_bool(row.get("featured")),
        external_id=row.get("external_id"),
    )


def get_csv_template() -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=TEMPLATE_HEADERS)
    writer.writeheader()
    writer.writerow(
        {
            "external_id": "store-001",
            "slug": "panama-city-hub",
            "name": "Panama City Hub",
            "business_type": "virtual-store",
            "status": "active",
            "description_short": "Sucursal principal",
            "address_line_1": "Avenida Balboa, Torre Central",
            "city": "Panama City",
            "country": "Panama",
            "latitude": "8.9824",
            "longitude": "-79.5199",
            "phone": "+507 300-1000",
            "email": "balboa@example.com",
            "website": "https://example.com/balboa",
            "opening_hours": '{"mon-fri":["08:00-18:00"]}',
            "services": "pickup|consulting",
            "featured": "true",
        }
    )
    return output.getvalue()


def _parse_json_field(value: str | None, *, default: dict) -> dict:
    if not value:
        return default
    parsed = json.loads(value)
    return parsed if isinstance(parsed, dict) else default


def _parse_list_field(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split("|") if item.strip()]


def _parse_bool(value: str | None) -> bool:
    if not value:
        return False
    return value.strip().lower() in {"1", "true", "yes", "y", "si"}


def _slugify(value: str) -> str:
    return "-".join(value.lower().strip().replace("/", " ").split())
