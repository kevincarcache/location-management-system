from typing import Literal

from pydantic import BaseModel, Field

BusinessType = Literal[
    "virtual-store",
    "nearby-event",
    "recycling-point",
    "academy",
    "technical-service",
]

LocationStatus = Literal["draft", "active", "archived"]


class LocationBase(BaseModel):
    slug: str
    name: str
    business_type: BusinessType
    status: LocationStatus = "active"
    description_short: str | None = None
    description_long: str | None = None
    address_line_1: str
    address_line_2: str | None = None
    city: str
    region: str | None = None
    country: str
    postal_code: str | None = None
    latitude: float
    longitude: float
    phone: str | None = None
    email: str | None = None
    website: str | None = None
    opening_hours: dict[str, list[str]] = Field(default_factory=dict)
    services: list[str] = Field(default_factory=list)
    featured: bool = False
    external_id: str | None = None


class LocationCreate(LocationBase):
    pass


class LocationUpdate(BaseModel):
    name: str | None = None
    status: LocationStatus | None = None
    description_short: str | None = None
    description_long: str | None = None
    address_line_1: str | None = None
    city: str | None = None
    country: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    featured: bool | None = None


class LocationRead(LocationBase):
    id: str

    model_config = {"from_attributes": True}
