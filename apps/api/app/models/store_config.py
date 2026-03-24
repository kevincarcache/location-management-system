from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class StoreConfig(Base):
    __tablename__ = "store_configs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid4()))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    brand_name: Mapped[str] = mapped_column(String(255))
    business_description: Mapped[str] = mapped_column(Text)
    theme_preset: Mapped[str] = mapped_column(String(64), default="serious-teal")
    business_type: Mapped[str] = mapped_column(String(64), default="virtual-store")
    logo_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    hero_title: Mapped[str] = mapped_column(String(255))
    hero_subtitle: Mapped[str] = mapped_column(Text)
    menu_label: Mapped[str] = mapped_column(String(255), default="Ubicaciones")
    footer_text: Mapped[str] = mapped_column(
        Text,
        default="Encuentra nuestras ubicaciones, eventos y puntos de servicio.",
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(UTC))
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
    )
