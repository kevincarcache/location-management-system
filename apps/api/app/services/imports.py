import csv
import json
from io import StringIO

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
    rows = _read_csv_rows(content)
    preview_rows: list[LocationImportPreviewRow] = []
    create_candidates = 0
    update_candidates = 0
    rejected_rows = 0

    for row_number, row in rows:
        try:
            payload = _build_location_payload(row)
            existing = _find_existing_location(db, payload.external_id, payload.slug)
            action = "update" if existing is not None else "create"
            if action == "update":
                update_candidates += 1
            else:
                create_candidates += 1
            preview_rows.append(
                LocationImportPreviewRow(
                    row_number=row_number,
                    action=action,
                    slug=payload.slug,
                    name=payload.name,
                    business_type=payload.business_type,
                )
            )
        except Exception as exc:
            rejected_rows += 1
            preview_rows.append(
                LocationImportPreviewRow(
                    row_number=row_number,
                    action="reject",
                    slug=row.get("slug"),
                    name=row.get("name"),
                    business_type=row.get("business_type"),
                    message=str(exc),
                )
            )

    total_rows = len(rows)
    valid_rows = total_rows - rejected_rows

    return LocationImportPreviewRead(
        filename=filename,
        required_columns=sorted(REQUIRED_COLUMNS),
        optional_columns=OPTIONAL_COLUMNS,
        total_rows=total_rows,
        valid_rows=valid_rows,
        create_candidates=create_candidates,
        update_candidates=update_candidates,
        rejected_rows=rejected_rows,
        rows=preview_rows,
    )


def import_locations_csv(db: Session, *, filename: str, content: bytes) -> LocationImportJobRead:
    rows = _read_csv_rows(content)
    job = create_import_job(db, filename=filename)
    created = 0
    updated = 0
    rejected = 0

    for row_number, row in rows:
        try:
            payload = _build_location_payload(row)
        except Exception as exc:
            rejected += 1
            add_import_error(
                db,
                job_id=job.id,
                row_number=row_number,
                message=str(exc),
                raw_row=json.dumps(row, ensure_ascii=True),
            )
            continue

        existing = _find_existing_location(db, payload.external_id, payload.slug)

        if existing is None:
            create_location(db, payload)
            created += 1
            continue

        update_location(
            db,
            existing,
            LocationUpdate(**payload.model_dump()),
        )
        updated += 1

    stored = update_import_job_counts(
        db,
        job,
        status="completed",
        created=created,
        updated=updated,
        rejected=rejected,
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


def _read_csv_rows(content: bytes) -> list[tuple[int, dict[str, str]]]:
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(StringIO(decoded))

    if not reader.fieldnames:
        raise ValueError("CSV file is missing a header row")

    missing = REQUIRED_COLUMNS.difference(reader.fieldnames)
    if missing:
        raise ValueError(f"CSV is missing required columns: {', '.join(sorted(missing))}")

    return list(enumerate(reader, start=2))


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
