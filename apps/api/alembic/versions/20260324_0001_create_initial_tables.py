"""create initial tables

Revision ID: 20260324_0001
Revises:
Create Date: 2026-03-24 09:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260324_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "admin_users",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("email", sa.String(length=255), nullable=False),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_admin_users_email"), "admin_users", ["email"], unique=True)

    op.create_table(
        "locations",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("slug", sa.String(length=255), nullable=False),
        sa.Column("external_id", sa.String(length=255), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("business_type", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("description_short", sa.Text(), nullable=True),
        sa.Column("description_long", sa.Text(), nullable=True),
        sa.Column("address_line_1", sa.String(length=255), nullable=False),
        sa.Column("address_line_2", sa.String(length=255), nullable=True),
        sa.Column("city", sa.String(length=128), nullable=False),
        sa.Column("region", sa.String(length=128), nullable=True),
        sa.Column("country", sa.String(length=128), nullable=False),
        sa.Column("postal_code", sa.String(length=32), nullable=True),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("phone", sa.String(length=64), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("website", sa.String(length=255), nullable=True),
        sa.Column("opening_hours", sa.JSON(), nullable=False),
        sa.Column("services", sa.JSON(), nullable=False),
        sa.Column("featured", sa.Boolean(), nullable=False),
        sa.Column("visible_from", sa.DateTime(), nullable=True),
        sa.Column("visible_until", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_locations_business_type"), "locations", ["business_type"], unique=False)
    op.create_index(op.f("ix_locations_city"), "locations", ["city"], unique=False)
    op.create_index(op.f("ix_locations_external_id"), "locations", ["external_id"], unique=False)
    op.create_index(op.f("ix_locations_name"), "locations", ["name"], unique=False)
    op.create_index(op.f("ix_locations_slug"), "locations", ["slug"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_locations_slug"), table_name="locations")
    op.drop_index(op.f("ix_locations_name"), table_name="locations")
    op.drop_index(op.f("ix_locations_external_id"), table_name="locations")
    op.drop_index(op.f("ix_locations_city"), table_name="locations")
    op.drop_index(op.f("ix_locations_business_type"), table_name="locations")
    op.drop_table("locations")
    op.drop_index(op.f("ix_admin_users_email"), table_name="admin_users")
    op.drop_table("admin_users")
