from logging import getLogger

from sqlalchemy.orm import Session

from app.repositories.imports import get_import_job
from app.schemas.imports import LocationImportJobRead, LocationImportPreviewRead
from app.services.location_imports import (
    build_import_plan,
    import_locations_from_plan,
    serialize_job,
    serialize_preview,
)
from app.services.location_imports import (
    get_csv_template as build_csv_template,
)

logger = getLogger(__name__)


def preview_locations_csv(
    db: Session,
    *,
    filename: str,
    content: bytes,
) -> LocationImportPreviewRead:
    plans = build_import_plan(db, content=content)
    logger.info("locations_import_preview filename=%s rows=%s", filename, len(plans))
    return serialize_preview(filename=filename, plans=plans)


def import_locations_csv(db: Session, *, filename: str, content: bytes) -> LocationImportJobRead:
    plans = build_import_plan(db, content=content)
    job = import_locations_from_plan(db, filename=filename, plans=plans)
    logger.info(
        "locations_import_completed filename=%s created=%s updated=%s rejected=%s",
        filename,
        job.created,
        job.updated,
        job.rejected,
    )
    return job


def get_import_job_result(db: Session, job_id: str) -> LocationImportJobRead | None:
    job = get_import_job(db, job_id)
    if job is None:
        return None
    return serialize_job(job)


def get_csv_template() -> str:
    return build_csv_template()
