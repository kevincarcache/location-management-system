from sqlalchemy.orm import Session

from app.core.config import settings
from app.repositories.store_configs import (
    create_store_config as create_store_config_record,
)
from app.repositories.store_configs import (
    get_first_store_config,
    get_store_config_by_id,
    get_store_config_by_slug,
)
from app.repositories.store_configs import (
    list_store_configs as list_store_config_records,
)
from app.repositories.store_configs import (
    update_store_config as update_store_config_record,
)
from app.schemas.store_config import (
    StoreConfigCreate,
    StoreConfigRead,
    StoreConfigUpdate,
)


def ensure_seed_store_config(db: Session) -> None:
    existing = get_store_config_by_slug(db, "default")
    if existing is not None:
        return

    create_store_config_record(
        db,
        slug="default",
        brand_name="Panama Service Network",
        business_description="Red comercial para eventos, sucursales y puntos de servicio.",
        theme_preset="serious-teal",
        business_type="virtual-store",
        logo_url=None,
        hero_title="Encuentra la sucursal ideal para tu próxima visita",
        hero_subtitle="Consulta horarios, ubicaciones y servicios disponibles en tiempo real.",
        menu_label="Sucursales",
        footer_text="Panama Service Network te acompaña con cobertura, atención y soporte.",
    )


def resolve_store_config(db: Session, requested_slug: str | None = None) -> StoreConfigRead:
    store_config = None
    if settings.storefront_slug:
        store_config = get_store_config_by_slug(db, settings.storefront_slug)
    if store_config is None and requested_slug:
        store_config = get_store_config_by_slug(db, requested_slug)
    if store_config is None:
        store_config = get_first_store_config(db)
    if store_config is None:
        raise ValueError("No store configuration is available")
    return StoreConfigRead.model_validate(store_config, from_attributes=True)


def list_store_configs(db: Session) -> list[StoreConfigRead]:
    return [
        StoreConfigRead.model_validate(store_config, from_attributes=True)
        for store_config in list_store_config_records(db)
    ]


def create_store_config(db: Session, payload: StoreConfigCreate) -> StoreConfigRead:
    created = create_store_config_record(db, **payload.model_dump())
    return StoreConfigRead.model_validate(created, from_attributes=True)


def update_store_config(
    db: Session,
    store_config_id: str,
    payload: StoreConfigUpdate,
) -> StoreConfigRead | None:
    store_config = get_store_config_by_id(db, store_config_id)
    if store_config is None:
        return None
    updated = update_store_config_record(db, store_config, **payload.model_dump(exclude_none=True))
    return StoreConfigRead.model_validate(updated, from_attributes=True)
