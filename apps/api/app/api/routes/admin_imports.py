from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_current_admin_user
from app.db.session import get_db
from app.schemas.imports import LocationImportJobRead, LocationImportPreviewRead
from app.services.imports import (
    get_csv_template,
    get_import_job_result,
    import_locations_csv,
    preview_locations_csv,
)

router = APIRouter(dependencies=[Depends(get_current_admin_user)])


@router.get("/locations/csv/template")
async def download_locations_template() -> Response:
    return Response(
        content=get_csv_template(),
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="locations-template.csv"'},
    )


@router.post("/locations/csv/preview", response_model=LocationImportPreviewRead)
async def preview_locations_import(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> LocationImportPreviewRead:
    try:
        return preview_locations_csv(
            db,
            filename=file.filename or "locations.csv",
            content=await file.read(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.post("/locations/csv", response_model=LocationImportJobRead, status_code=202)
async def upload_locations_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> LocationImportJobRead:
    try:
        return import_locations_csv(
            db,
            filename=file.filename or "locations.csv",
            content=await file.read(),
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc


@router.get("/{job_id}", response_model=LocationImportJobRead)
async def get_import_job(job_id: str, db: Session = Depends(get_db)) -> LocationImportJobRead:
    job = get_import_job_result(db, job_id)
    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Import job not found")
    return job
