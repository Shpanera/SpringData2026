from __future__ import annotations

from geoalchemy2 import WKTElement
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from src.lab6_app.common.db import Base
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

    def get_territory(self, db: Session, territory_id: int):
        stmt = self._territory_select().where(Territory.id == territory_id)
        return db.execute(stmt).mappings().first()

    def list_territories(self, db: Session, limit: int = 100, offset: int = 0):
        stmt = self._territory_select().order_by(Territory.id).limit(limit).offset(offset)
        return db.execute(stmt).mappings().all()

    def create_territory(self, db: Session, data: TerritoryCreate):
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

    def update_territory(self, db: Session, territory_id: int, data: TerritoryUpdate):
        territory = db.get(Territory, territory_id)
        if territory is None:
            return None

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
            return False
        db.delete(territory)
        db.commit()
        return True

    def list_intersecting_territories(self, db: Session, wkt: str, limit: int = 100, offset: int = 0):
        search_geom = WKTElement(wkt, srid=4326)
        stmt = (
            self._territory_select()
            .where(func.ST_Intersects(Territory.geom, search_geom))
            .order_by(Territory.id)
            .limit(limit)
            .offset(offset)
        )
        return db.execute(stmt).mappings().all()

    def create_metric(self, db: Session, territory_id: int, data: TerritoryMetricCreate):
        metric = TerritoryMetric(
            territory_id=territory_id,
            year=data.year,
            population=data.population,
            area_km2=data.area_km2,
            source=data.source,
        )
        db.add(metric)
        db.commit()
        db.refresh(metric)
        return metric

    def list_metrics_by_territory(self, db: Session, territory_id: int):
        stmt = (
            select(TerritoryMetric)
            .where(TerritoryMetric.territory_id == territory_id)
            .order_by(TerritoryMetric.year)
        )
        return db.scalars(stmt).all()

    def get_metric(self, db: Session, metric_id: int):
        return db.get(TerritoryMetric, metric_id)

    def update_metric(self, db: Session, metric_id: int, data: TerritoryMetricUpdate):
        metric = db.get(TerritoryMetric, metric_id)
        if metric is None:
            return None
        payload = data.model_dump(exclude_unset=True)
        for field, value in payload.items():
            setattr(metric, field, value)
        db.commit()
        db.refresh(metric)
        return metric

    def delete_metric(self, db: Session, metric_id: int) -> bool:
        metric = db.get(TerritoryMetric, metric_id)
        if metric is None:
            return False
        db.delete(metric)
        db.commit()
        return True
