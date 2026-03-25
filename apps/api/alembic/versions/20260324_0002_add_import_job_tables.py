"""add import job tables

Revision ID: 20260324_0002
Revises: 20260324_0001
Create Date: 2026-03-24 12:00:00
"""

from alembic import op
import sqlalchemy as sa


revision = "20260324_0002"
down_revision = "20260324_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "location_import_jobs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("filename", sa.String(length=255), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created", sa.Integer(), nullable=False),
        sa.Column("updated", sa.Integer(), nullable=False),
        sa.Column("rejected", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "location_import_row_errors",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("job_id", sa.String(length=36), nullable=False),
        sa.Column("row_number", sa.Integer(), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("raw_row", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["job_id"], ["location_import_jobs.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_location_import_row_errors_job_id"),
        "location_import_row_errors",
        ["job_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_location_import_row_errors_job_id"), table_name="location_import_row_errors")
    op.drop_table("location_import_row_errors")
    op.drop_table("location_import_jobs")
