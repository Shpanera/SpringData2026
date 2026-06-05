from __future__ import annotations

from geoalchemy2 import WKTElement
from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.lab6_app.exceptions import (
    MetricAlreadyExistsError,
    MetricNotFoundError,
    TerritoryNotFoundError,
)
from src.lab6_app.schemas.territories import (
    TerritoryCreate,
    TerritoryMetricCreate,
    TerritoryMetricUpdate,
    TerritoryUpdate,
)
from src.lab6_app.territories_models import Territory, TerritoryMetric


class TerritoryService:
    def _territory_select(self):
        return select(
            Territory.id,
            Territory.name,
            Territory.territory_type,
            Territory.level,
            Territory.description,
            func.ST_AsText(Territory.geom).label("geom_wkt"),
            Territory.created_at,
        )

    def get_territory(self, db: Session, territory_id: int) -> dict:
        stmt = self._territory_select().where(Territory.id == territory_id)
        territory = db.execute(stmt).mappings().first()
        if territory is None:
            raise TerritoryNotFoundError(f"Territory with id={territory_id} not found")
        return dict(territory)

    def get_territory_or_none(self, db: Session, territory_id: int) -> dict | None:
        stmt = self._territory_select().where(Territory.id == territory_id)
        territory = db.execute(stmt).mappings().first()
        return dict(territory) if territory else None

    def list_territories(self, db: Session, limit: int = 100, offset: int = 0) -> list[dict]:
        stmt = self._territory_select().order_by(Territory.id).limit(limit).offset(offset)
        return [dict(row) for row in db.execute(stmt).mappings().all()]

    def create_territory(self, db: Session, data: TerritoryCreate) -> dict:
        territory = Territory(
            name=data.name,
            territory_type=data.territory_type,
            level=data.level,
            description=data.description,
            geom=WKTElement(data.geom_wkt, srid=4326),
        )
        db.add(territory)
        db.commit()
        db.refresh(territory)
        return self.get_territory(db, territory.id)

    def update_territory(self, db: Session, territory_id: int, data: TerritoryUpdate) -> dict:
        territory = db.get(Territory, territory_id)
        if territory is None:
            raise TerritoryNotFoundError(f"Territory with id={territory_id} not found")

        payload = data.model_dump(exclude_unset=True)
        geom_wkt = payload.pop("geom_wkt", None)
        if geom_wkt is not None:
            territory.geom = WKTElement(geom_wkt, srid=4326)

        for field, value in payload.items():
            setattr(territory, field, value)

        db.commit()
        db.refresh(territory)
        return self.get_territory(db, territory.id)

    def delete_territory(self, db: Session, territory_id: int) -> bool:
        territory = db.get(Territory, territory_id)
        if territory is None:
            raise TerritoryNotFoundError(f"Territory with id={territory_id} not found")
        db.delete(territory)
        db.commit()
        return True

    def list_intersecting_territories(
        self, db: Session, wkt: str, limit: int = 100, offset: int = 0
    ) -> list[dict]:
        search_geom = WKTElement(wkt, srid=4326)
        stmt = (
            self._territory_select()
            .where(func.ST_Intersects(Territory.geom, search_geom))
            .order_by(Territory.id)
            .limit(limit)
            .offset(offset)
        )
        return [dict(row) for row in db.execute(stmt).mappings().all()]

    def get_metric(self, db: Session, metric_id: int) -> TerritoryMetric:
        metric = db.get(TerritoryMetric, metric_id)
        if metric is None:
            raise MetricNotFoundError(f"Metric with id={metric_id} not found")
        return metric

    def get_metric_or_none(self, db: Session, metric_id: int) -> TerritoryMetric | None:
        return db.get(TerritoryMetric, metric_id)

    def get_metric_by_territory_and_year(
        self, db: Session, territory_id: int, year: int
    ) -> TerritoryMetric | None:
        stmt = select(TerritoryMetric).where(
            TerritoryMetric.territory_id == territory_id,
            TerritoryMetric.year == year,
        )
        return db.scalars(stmt).first()

    def create_metric(self, db: Session, territory_id: int, data: TerritoryMetricCreate) -> TerritoryMetric:
        existing_metric = self.get_metric_by_territory_and_year(db, territory_id, data.year)
        if existing_metric is not None:
            raise MetricAlreadyExistsError(
                f"Metric for territory_id={territory_id} and year={data.year} already exists"
            )

        metric = TerritoryMetric(
            territory_id=territory_id,
            year=data.year,
            population=data.population,
            area_km2=data.area_km2,
            source=data.source,
        )
        db.add(metric)
        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise MetricAlreadyExistsError(
                f"Metric for territory_id={territory_id} and year={data.year} already exists"
            ) from exc
        db.refresh(metric)
        return metric

    def list_metrics_by_territory(self, db: Session, territory_id: int) -> list[TerritoryMetric]:
        stmt = (
            select(TerritoryMetric)
            .where(TerritoryMetric.territory_id == territory_id)
            .order_by(TerritoryMetric.year)
        )
        return list(db.scalars(stmt).all())

    def update_metric(self, db: Session, territory_id: int, metric_id: int, data: TerritoryMetricUpdate) -> TerritoryMetric:
        metric = self.get_metric(db=db, metric_id=metric_id)
        if metric.territory_id != territory_id:
            raise MetricNotFoundError(f"Metric with id={metric_id} not found for territory_id={territory_id}")

        target_year = data.year if data.year is not None else metric.year
        existing_metric = self.get_metric_by_territory_and_year(db, territory_id, target_year)
        if existing_metric is not None and existing_metric.id != metric_id:
            raise MetricAlreadyExistsError(
                f"Metric for territory_id={territory_id} and year={target_year} already exists"
            )

        payload = data.model_dump(exclude_unset=True)
        for field, value in payload.items():
            setattr(metric, field, value)

        try:
            db.commit()
        except IntegrityError as exc:
            db.rollback()
            raise MetricAlreadyExistsError(
                f"Metric for territory_id={territory_id} and year={target_year} already exists"
            ) from exc

        db.refresh(metric)
        return metric

    def delete_metric(self, db: Session, territory_id: int, metric_id: int) -> bool:
        metric = self.get_metric(db=db, metric_id=metric_id)
        if metric.territory_id != territory_id:
            raise MetricNotFoundError(f"Metric with id={metric_id} not found for territory_id={territory_id}")
        db.delete(metric)
        db.commit()
        return True
