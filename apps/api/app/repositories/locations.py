from sqlalchemy import Select, or_, select
from sqlalchemy.orm import Session

from app.models.location import Location
from app.schemas.location import LocationCreate, LocationUpdate


def build_locations_query(
    *,
    query: str | None = None,
    business_type: str | None = None,
    public_only: bool = False,
) -> Select[tuple[Location]]:
    statement = select(Location).order_by(Location.featured.desc(), Location.name.asc())

    if public_only:
        statement = statement.where(Location.status == "active")

    if query:
        normalized = f"%{query.strip()}%"
        statement = statement.where(
            or_(
                Location.name.ilike(normalized),
                Location.city.ilike(normalized),
                Location.address_line_1.ilike(normalized),
            )
        )

    if business_type:
        statement = statement.where(Location.business_type == business_type)

    return statement


def list_locations(
    db: Session,
    *,
    query: str | None = None,
    business_type: str | None = None,
    public_only: bool = False,
) -> list[Location]:
    statement = build_locations_query(
        query=query,
        business_type=business_type,
        public_only=public_only,
    )
    return list(db.scalars(statement).all())


def get_location_by_id(db: Session, location_id: str) -> Location | None:
    statement = select(Location).where(Location.id == location_id)
    return db.scalar(statement)


def get_location_by_slug(db: Session, slug: str, *, public_only: bool = False) -> Location | None:
    statement = select(Location).where(Location.slug == slug)
    if public_only:
        statement = statement.where(Location.status == "active")
    return db.scalar(statement)


def get_location_by_external_id(db: Session, external_id: str) -> Location | None:
    statement = select(Location).where(Location.external_id == external_id)
    return db.scalar(statement)


def create_location(db: Session, payload: LocationCreate) -> Location:
    location = Location(**payload.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def update_location(db: Session, location: Location, payload: LocationUpdate) -> Location:
    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(location, field, value)

    db.add(location)
    db.commit()
    db.refresh(location)
    return location


def delete_location(db: Session, location: Location) -> None:
    db.delete(location)
    db.commit()
