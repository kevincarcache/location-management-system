from uuid import uuid4

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class LocationImportRowError(Base):
    __tablename__ = "location_import_row_errors"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("location_import_jobs.id", ondelete="CASCADE"),
        index=True,
    )
    row_number: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(Text)
    raw_row: Mapped[str] = mapped_column(Text)

    job = relationship("LocationImportJob", back_populates="errors")
