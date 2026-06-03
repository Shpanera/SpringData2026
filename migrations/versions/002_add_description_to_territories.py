"""add description to territories

Revision ID: 002_add_description_to_territories
Revises: 001_create_territories_and_coverage_results
Create Date: 2026-06-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "002_add_description_to_territories"
down_revision: Union[str, None] = "001_create_territories_and_coverage_results"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "territories",
        sa.Column("description", sa.String(length=500), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("territories", "description")
