from dataclasses import dataclass

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash
from app.repositories.admin_users import create_admin_user, get_admin_user_by_email


@dataclass
class SeedAdminUser:
    email: str
    hashed_password: str
    full_name: str


def get_seed_admin_user() -> SeedAdminUser:
    return SeedAdminUser(
        email=settings.admin_email,
        hashed_password=get_password_hash(settings.admin_password),
        full_name=settings.admin_full_name,
    )


def ensure_seed_admin_user(db: Session) -> None:
    seed_admin = get_seed_admin_user()
    existing_admin = get_admin_user_by_email(db, seed_admin.email)
    if existing_admin:
        return

    create_admin_user(
        db,
        email=seed_admin.email,
        full_name=seed_admin.full_name,
        hashed_password=seed_admin.hashed_password,
    )
    db.commit()
