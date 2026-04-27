from dataclasses import dataclass

from app.schemas.location import LocationCreate

REQUIRED_COLUMNS = {
    "external_id",
    "name",
    "business_type",
    "address_line_1",
    "city",
    "country",
    "latitude",
    "longitude",
}
OPTIONAL_COLUMNS = [
    "slug",
    "status",
    "description_short",
    "description_long",
    "address_line_2",
    "region",
    "postal_code",
    "phone",
    "email",
    "website",
    "opening_hours",
    "services",
    "featured",
]
TEMPLATE_HEADERS = [
    "external_id",
    "slug",
    "name",
    "business_type",
    "status",
    "description_short",
    "description_long",
    "address_line_1",
    "address_line_2",
    "city",
    "region",
    "country",
    "postal_code",
    "latitude",
    "longitude",
    "phone",
    "email",
    "website",
    "opening_hours",
    "services",
    "featured",
]


@dataclass(slots=True)
class ParsedImportRow:
    row_number: int
    raw: dict[str, str]


@dataclass(slots=True)
class ImportActionPlan:
    row_number: int
    raw: dict[str, str]
    payload: LocationCreate | None
    action: str
    message: str | None = None
