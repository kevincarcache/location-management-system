"""add store configs

Revision ID: 20260324_0003
Revises: 20260324_0002
Create Date: 2026-03-24 16:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260324_0003"
down_revision = "20260324_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if "store_configs" not in inspector.get_table_names():
        op.create_table(
            "store_configs",
            sa.Column("id", sa.String(length=36), nullable=False),
            sa.Column("slug", sa.String(length=100), nullable=False),
            sa.Column("brand_name", sa.String(length=255), nullable=False),
            sa.Column("business_description", sa.Text(), nullable=False),
            sa.Column("theme_preset", sa.String(length=64), nullable=False),
            sa.Column("business_type", sa.String(length=64), nullable=False),
            sa.Column("logo_url", sa.String(length=500), nullable=True),
            sa.Column("hero_title", sa.String(length=255), nullable=False),
            sa.Column("hero_subtitle", sa.Text(), nullable=False),
            sa.Column("menu_label", sa.String(length=255), nullable=False),
            sa.Column("footer_text", sa.Text(), nullable=False),
            sa.Column("created_at", sa.DateTime(), nullable=False),
            sa.Column("updated_at", sa.DateTime(), nullable=False),
            sa.PrimaryKeyConstraint("id"),
        )

    indexes = {index["name"] for index in inspector.get_indexes("store_configs")}
    index_name = op.f("ix_store_configs_slug")
    if index_name not in indexes:
        op.create_index(index_name, "store_configs", ["slug"], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)
    if "store_configs" not in inspector.get_table_names():
        return

    indexes = {index["name"] for index in inspector.get_indexes("store_configs")}
    index_name = op.f("ix_store_configs_slug")
    if index_name in indexes:
        op.drop_index(index_name, table_name="store_configs")
    op.drop_table("store_configs")
