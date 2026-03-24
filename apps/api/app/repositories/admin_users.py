from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.admin_user import AdminUser


def get_admin_user_by_email(db: Session, email: str) -> AdminUser | None:
    statement = select(AdminUser).where(AdminUser.email == email)
    return db.scalar(statement)


def create_admin_user(
    db: Session,
    *,
    email: str,
    full_name: str,
    hashed_password: str,
) -> AdminUser:
    admin_user = AdminUser(
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
    )
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    return admin_user
