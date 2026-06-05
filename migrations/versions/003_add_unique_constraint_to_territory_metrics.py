"""add unique constraint to territory_metrics

Revision ID: 003_add_unique_constraint_to_territory_metrics
Revises: 002_add_description_to_territories
Create Date: 2026-06-05
"""

from typing import Sequence, Union

from alembic import op


revision: str = "003_add_unique_constraint_to_territory_metrics"
down_revision: Union[str, None] = "002_add_description_to_territories"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        DELETE FROM territory_metrics t1
        USING territory_metrics t2
        WHERE t1.id < t2.id
          AND t1.territory_id = t2.territory_id
          AND t1.year = t2.year;
        """
    )

    op.create_unique_constraint(
        "uq_territory_metrics_territory_year",
        "territory_metrics",
        ["territory_id", "year"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "uq_territory_metrics_territory_year",
        "territory_metrics",
        type_="unique",
    )
