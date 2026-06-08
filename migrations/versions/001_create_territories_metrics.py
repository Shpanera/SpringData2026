"""create territories and buffer coverage results

Revision ID: 001_create_territories_and_coverage_results
Revises:
Create Date: 2026-06-03
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from geoalchemy2 import Geometry


revision: str = "001_create_territories_and_coverage_results"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Включаем PostGIS, если ещё не включён
    op.execute("CREATE EXTENSION IF NOT EXISTS postgis")

    # Базовая таблица территорий
    op.create_table(
        "territories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("territory_type", sa.String(length=100), nullable=False),
        sa.Column("level", sa.Integer(), nullable=False),
        sa.Column(
            "geom",
            Geometry(
                geometry_type="MULTIPOLYGON",
                srid=4326,
                spatial_index=False,
            ),
            nullable=False,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.CheckConstraint("level >= 0", name="ck_territories_level_non_negative"),
    )

    op.create_index(
        "idx_territories_geom",
        "territories",
        ["geom"],
        postgresql_using="gist",
    )

    # Таблица результатов геоанализа покрытия буферами
    op.create_table(
        "buffer_coverage_results",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("territory_id", sa.Integer(), nullable=False),
        sa.Column("analysis_date", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("radius_m", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("coverage_area_m2", sa.Numeric(precision=18, scale=2), nullable=True),
        sa.Column("coverage_ratio", sa.Numeric(precision=6, scale=4), nullable=True),
        sa.Column("objects_count", sa.Integer(), nullable=True),
        sa.Column("note", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["territory_id"],
            ["territories.id"],
            name="fk_buffer_coverage_results_territory_id",
            ondelete="CASCADE",
        ),
    )

    op.create_index(
        "idx_buffer_coverage_results_territory_id",
        "buffer_coverage_results",
        ["territory_id"],
    )

    # Немного тестовых данных — можно привязать к Санкт‑Петербургу
    op.execute(
        """
        INSERT INTO territories (id, name, territory_type, level, geom)
        VALUES
        (
            1,
            'Центральный тестовый район',
            'district',
            1,
            ST_GeomFromText(
                'MULTIPOLYGON(((30.30 59.90, 30.45 59.90, 30.45 60.00, 30.30 60.00, 30.30 59.90)))',
                4326
            )
        ),
        (
            2,
            'Периферийный тестовый район',
            'district',
            1,
            ST_GeomFromText(
                'MULTIPOLYGON(((30.45 59.90, 30.60 59.90, 30.60 60.00, 30.45 60.00, 30.45 59.90)))',
                4326
            )
        );
        """
    )

    # Здесь данные — как будто результат работы buffer_coverage
    op.execute(
        """
        INSERT INTO buffer_coverage_results
            (territory_id, radius_m, coverage_area_m2, coverage_ratio, objects_count, note)
        VALUES
            (1, 300.0, 250000.00, 0.72, 15, 'demo result for Central district'),
            (2, 300.0, 180000.00, 0.55, 10, 'demo result for Peripheral district');
        """
    )


def downgrade() -> None:
    op.drop_index(
        "idx_buffer_coverage_results_territory_id",
        table_name="buffer_coverage_results",
    )
    op.drop_table("buffer_coverage_results")

    op.drop_index("idx_territories_geom", table_name="territories")
    op.drop_table("territories")
