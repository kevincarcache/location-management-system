import json

from sqlalchemy.orm import Session

from app.repositories.imports import (
    add_import_error,
    create_import_job,
    get_import_job,
    update_import_job_counts,
)
from app.repositories.locations import create_location, update_location
from app.schemas.imports import LocationImportJobRead, LocationImportRowErrorRead
from app.schemas.location import LocationUpdate
from app.services.location_imports.models import ImportActionPlan
from app.services.location_imports.planner import find_existing_location


def import_locations_from_plan(
    db: Session,
    *,
    filename: str,
    plans: list[ImportActionPlan],
) -> LocationImportJobRead:
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

        existing = find_existing_location(db, plan.payload.external_id, plan.payload.slug)
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
    hydrated = get_import_job(db, stored.id)
    return serialize_job(hydrated or stored)


def serialize_job(job) -> LocationImportJobRead:
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
