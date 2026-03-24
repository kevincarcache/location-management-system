from sqlalchemy.orm import Session

from app.db.session import Base, engine
from app.services.locations import ensure_seed_locations
from app.services.seed import ensure_seed_admin_user
from app.services.store_configs import ensure_seed_store_config


def init_db(*, db: Session | None = None) -> None:
    Base.metadata.create_all(bind=engine)
    if db is not None:
        ensure_seed_admin_user(db)
        ensure_seed_store_config(db)
        ensure_seed_locations(db)
