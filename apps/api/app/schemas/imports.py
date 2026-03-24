from typing import Literal

from pydantic import BaseModel


class LocationImportPreviewRow(BaseModel):
    row_number: int
    action: Literal["create", "update", "reject"]
    slug: str | None = None
    name: str | None = None
    business_type: str | None = None
    message: str | None = None


class LocationImportPreviewRead(BaseModel):
    filename: str
    required_columns: list[str]
    optional_columns: list[str]
    total_rows: int
    valid_rows: int
    create_candidates: int
    update_candidates: int
    rejected_rows: int
    rows: list[LocationImportPreviewRow]


class LocationImportRowErrorRead(BaseModel):
    id: str
    row_number: int
    message: str
    raw_row: str


class LocationImportJobRead(BaseModel):
    id: str
    filename: str
    status: Literal["pending", "processing", "completed", "failed"]
    created: int
    updated: int
    rejected: int
    errors: list[LocationImportRowErrorRead] = []
