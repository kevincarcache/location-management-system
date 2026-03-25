import csv
import json
from dataclasses import dataclass
from io import StringIO
from logging import getLogger

from sqlalchemy.orm import Session

from app.repositories.imports import (
    add_import_error,
    create_import_job,
    get_import_job,
    update_import_job_counts,
)
from app.repositories.locations import (
    create_location,
    get_location_by_external_id,
    get_location_by_slug,
    update_location,
)
from app.schemas.imports import (
    LocationImportJobRead,
    LocationImportPreviewRead,
    LocationImportPreviewRow,
    LocationImportRowErrorRead,
)
from app.schemas.location import LocationCreate, LocationUpdate

logger = getLogger(__name__)

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


def _serialize_job(job) -> LocationImportJobRead:
    return LocationImportJobRead(
        id=job.id,
        filename=job.filename,
        status=job.status,
        created=job.created,
        updated=job.updated,
        rejected=job.rejected,
        errors=[
            LocationImportRowErrorRead(
                id=error.id,
                row_number=error.row_number,
                message=error.message,
                raw_row=error.raw_row,
            )
            for error in getattr(job, "errors", [])
        ],
    )


def preview_locations_csv(
    db: Session,
    *,
    filename: str,
    content: bytes,
) -> LocationImportPreviewRead:
    plans = _build_import_plan(db, content=content)
    logger.info("locations_import_preview filename=%s rows=%s", filename, len(plans))
    return _serialize_preview(filename=filename, plans=plans)


def import_locations_csv(db: Session, *, filename: str, content: bytes) -> LocationImportJobRead:
    plans = _build_import_plan(db, content=content)
    job = create_import_job(db, filename=filename)
    created = 0
    updated = 0
    rejected = 0

    for plan in plans:
        if plan.action == "reject" or plan.payload is None:
            rejected += 1
            add_import_error(
                db,
                job_id=job.id,
                row_number=plan.row_number,
                message=plan.message or "Rejected row",
                raw_row=json.dumps(plan.raw, ensure_ascii=True),
            )
            continue

        if plan.action == "create":
            create_location(db, plan.payload)
            created += 1
            continue

        existing = _find_existing_location(db, plan.payload.external_id, plan.payload.slug)
        if existing is None:
            create_location(db, plan.payload)
            created += 1
            continue

        update_location(db, existing, LocationUpdate(**plan.payload.model_dump()))
        updated += 1

    stored = update_import_job_counts(
        db,
        job,
        status="completed",
        created=created,
        updated=updated,
        rejected=rejected,
    )
    db.commit()
    logger.info(
        "locations_import_completed filename=%s created=%s updated=%s rejected=%s",
        filename,
        created,
        updated,
        rejected,
    )
    hydrated = get_import_job(db, stored.id)
    return _serialize_job(hydrated or stored)


def get_import_job_result(db: Session, job_id: str) -> LocationImportJobRead | None:
    job = get_import_job(db, job_id)
    if job is None:
        return None
    return _serialize_job(job)


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


def _serialize_preview(
    *,
    filename: str,
    plans: list[ImportActionPlan],
) -> LocationImportPreviewRead:
    create_candidates = sum(plan.action == "create" for plan in plans)
    update_candidates = sum(plan.action == "update" for plan in plans)
    rejected_rows = sum(plan.action == "reject" for plan in plans)

    return LocationImportPreviewRead(
        filename=filename,
        required_columns=sorted(REQUIRED_COLUMNS),
        optional_columns=OPTIONAL_COLUMNS,
        total_rows=len(plans),
        valid_rows=len(plans) - rejected_rows,
        create_candidates=create_candidates,
        update_candidates=update_candidates,
        rejected_rows=rejected_rows,
        rows=[
            LocationImportPreviewRow(
                row_number=plan.row_number,
                action=plan.action,
                slug=plan.payload.slug if plan.payload else plan.raw.get("slug"),
                name=plan.payload.name if plan.payload else plan.raw.get("name"),
                business_type=(
                    plan.payload.business_type if plan.payload else plan.raw.get("business_type")
                ),
                message=plan.message,
            )
            for plan in plans
        ],
    )


def _build_import_plan(db: Session, *, content: bytes) -> list[ImportActionPlan]:
    parsed_rows = _read_csv_rows(content)
    return [_classify_import_row(db, parsed_row) for parsed_row in parsed_rows]


def _read_csv_rows(content: bytes) -> list[ParsedImportRow]:
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


def _classify_import_row(db: Session, parsed_row: ParsedImportRow) -> ImportActionPlan:
    try:
        payload = _build_location_payload(parsed_row.raw)
        existing = _find_existing_location(db, payload.external_id, payload.slug)
        return ImportActionPlan(
            row_number=parsed_row.row_number,
            raw=parsed_row.raw,
            payload=payload,
            action="update" if existing is not None else "create",
        )
    except Exception as exc:
        return ImportActionPlan(
            row_number=parsed_row.row_number,
            raw=parsed_row.raw,
            payload=None,
            action="reject",
            message=str(exc),
        )


def _build_location_payload(row: dict[str, str]) -> LocationCreate:
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


def _find_existing_location(db: Session, external_id: str | None, slug: str):
    existing = None
    if external_id:
        existing = get_location_by_external_id(db, external_id)
    if existing is None:
        existing = get_location_by_slug(db, slug)
    return existing


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
