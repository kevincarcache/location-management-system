from fastapi import APIRouter, UploadFile

from app.schemas.imports import LocationImportJobRead

router = APIRouter()


@router.post("/locations/csv", response_model=LocationImportJobRead, status_code=202)
async def upload_locations_csv(file: UploadFile) -> LocationImportJobRead:
    return LocationImportJobRead(
        id="preview-import-job",
        filename=file.filename or "locations.csv",
        status="pending",
        created=0,
        updated=0,
        rejected=0,
    )


@router.get("/{job_id}", response_model=LocationImportJobRead)
async def get_import_job(job_id: str) -> LocationImportJobRead:
    return LocationImportJobRead(
        id=job_id,
        filename="locations.csv",
        status="pending",
        created=0,
        updated=0,
        rejected=0,
    )

