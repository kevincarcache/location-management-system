from sqlalchemy.orm import Session

from app.repositories.locations import get_location_by_external_id, get_location_by_slug
from app.schemas.imports import LocationImportPreviewRead, LocationImportPreviewRow
from app.services.location_imports.models import (
    OPTIONAL_COLUMNS,
    REQUIRED_COLUMNS,
    ImportActionPlan,
    ParsedImportRow,
)
from app.services.location_imports.parser import build_location_payload, read_csv_rows


def build_import_plan(db: Session, *, content: bytes) -> list[ImportActionPlan]:
    parsed_rows = read_csv_rows(content)
    return [classify_import_row(db, parsed_row) for parsed_row in parsed_rows]


def classify_import_row(db: Session, parsed_row: ParsedImportRow) -> ImportActionPlan:
    try:
        payload = build_location_payload(parsed_row.raw)
        existing = find_existing_location(db, payload.external_id, payload.slug)
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


def serialize_preview(
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


def find_existing_location(db: Session, external_id: str | None, slug: str):
    existing = None
    if external_id:
        existing = get_location_by_external_id(db, external_id)
    if existing is None:
        existing = get_location_by_slug(db, slug)
    return existing
