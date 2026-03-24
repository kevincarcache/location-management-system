from pydantic import BaseModel

from app.schemas.location import BusinessType


class StoreConfigBase(BaseModel):
    slug: str
    brand_name: str
    business_description: str
    theme_preset: str = "serious-teal"
    business_type: BusinessType
    logo_url: str | None = None
    hero_title: str
    hero_subtitle: str
    menu_label: str = "Ubicaciones"
    footer_text: str = "Encuentra nuestras ubicaciones, eventos y puntos de servicio."


class StoreConfigCreate(StoreConfigBase):
    pass


class StoreConfigUpdate(BaseModel):
    slug: str | None = None
    brand_name: str | None = None
    business_description: str | None = None
    theme_preset: str | None = None
    business_type: BusinessType | None = None
    logo_url: str | None = None
    hero_title: str | None = None
    hero_subtitle: str | None = None
    menu_label: str | None = None
    footer_text: str | None = None


class StoreConfigRead(StoreConfigBase):
    id: str

    model_config = {"from_attributes": True}
