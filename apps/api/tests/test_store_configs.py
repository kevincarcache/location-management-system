from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import settings
from app.db.session import Base
from app.schemas.store_config import StoreConfigCreate
from app.services.store_configs import (
    create_store_config,
    ensure_seed_store_config,
    resolve_store_config,
)


def make_db() -> Session:
    engine = create_engine("sqlite+pysqlite:///:memory:", future=True)
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False, class_=Session)
    return testing_session()


def test_seed_creates_default_store_config() -> None:
    db = make_db()

    ensure_seed_store_config(db)
    resolved = resolve_store_config(db)

    assert resolved.slug == "default"
    assert resolved.business_type == "virtual-store"


def test_resolve_store_config_prefers_env_then_requested_then_first_record() -> None:
    db = make_db()
    original_storefront_slug = settings.storefront_slug

    ensure_seed_store_config(db)
    create_store_config(
        db,
        StoreConfigCreate(
            slug="events",
            brand_name="Event Network",
            business_description="Agenda pública de eventos.",
            theme_preset="graphite-sand",
            business_type="nearby-event",
            logo_url=None,
            hero_title="Eventos y experiencias",
            hero_subtitle="Encuentra actividades activas.",
            menu_label="Eventos",
            footer_text="Agenda pública de actividades y encuentros.",
        ),
    )

    try:
        settings.storefront_slug = "default"
        resolved = resolve_store_config(db, requested_slug="events")
        assert resolved.slug == "default"
    finally:
        settings.storefront_slug = original_storefront_slug

    resolved_from_request = resolve_store_config(db, requested_slug="events")
    assert resolved_from_request.slug == "events"
