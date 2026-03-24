from typing import Literal

from pydantic import BaseModel


class LocationImportJobRead(BaseModel):
    id: str
    filename: str
    status: Literal["pending", "processing", "completed", "failed"]
    created: int
    updated: int
    rejected: int

