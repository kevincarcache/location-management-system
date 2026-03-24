from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.store_config import StoreConfig


def list_store_configs(db: Session) -> list[StoreConfig]:
    return list(db.scalars(select(StoreConfig).order_by(StoreConfig.slug.asc())).all())


def get_store_config_by_id(db: Session, store_config_id: str) -> StoreConfig | None:
    return db.scalar(select(StoreConfig).where(StoreConfig.id == store_config_id))


def get_store_config_by_slug(db: Session, slug: str) -> StoreConfig | None:
    return db.scalar(select(StoreConfig).where(StoreConfig.slug == slug))


def get_first_store_config(db: Session) -> StoreConfig | None:
    return db.scalar(select(StoreConfig).order_by(StoreConfig.created_at.asc()))


def create_store_config(db: Session, **kwargs) -> StoreConfig:
    store_config = StoreConfig(**kwargs)
    db.add(store_config)
    db.commit()
    db.refresh(store_config)
    return store_config


def update_store_config(db: Session, store_config: StoreConfig, **kwargs) -> StoreConfig:
    for field, value in kwargs.items():
        setattr(store_config, field, value)
    db.add(store_config)
    db.commit()
    db.refresh(store_config)
    return store_config
