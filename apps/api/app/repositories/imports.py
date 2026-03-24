from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.location_import_job import LocationImportJob
from app.models.location_import_row_error import LocationImportRowError


def create_import_job(db: Session, *, filename: str) -> LocationImportJob:
    job = LocationImportJob(filename=filename, status="processing")
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


def add_import_error(
    db: Session,
    *,
    job_id: str,
    row_number: int,
    message: str,
    raw_row: str,
) -> LocationImportRowError:
    error = LocationImportRowError(
        job_id=job_id,
        row_number=row_number,
        message=message,
        raw_row=raw_row,
    )
    db.add(error)
    db.commit()
    db.refresh(error)
    return error


def get_import_job(db: Session, job_id: str) -> LocationImportJob | None:
    statement = (
        select(LocationImportJob)
        .where(LocationImportJob.id == job_id)
        .options(selectinload(LocationImportJob.errors))
    )
    return db.scalar(statement)


def update_import_job_counts(
    db: Session,
    job: LocationImportJob,
    *,
    status: str,
    created: int,
    updated: int,
    rejected: int,
) -> LocationImportJob:
    job.status = status
    job.created = created
    job.updated = updated
    job.rejected = rejected
    db.add(job)
    db.commit()
    db.refresh(job)
    return job
