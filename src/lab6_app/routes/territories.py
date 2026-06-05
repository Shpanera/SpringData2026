from __future__ import annotations

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from src.lab6_app.common.db import get_db
from src.lab6_app.dependencies import get_territory_service
from src.lab6_app.schemas.territories import (
    TerritoryCreate,
    TerritoryMetricCreate,
    TerritoryMetricRead,
    TerritoryMetricUpdate,
    TerritoryRead,
    TerritoryUpdate,
)
from src.lab6_app.services.territory_service import TerritoryService

router = APIRouter(prefix="/territories", tags=["territories"])


@router.post("", response_model=TerritoryRead, status_code=status.HTTP_201_CREATED)
def create_territory(
    data: TerritoryCreate,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> TerritoryRead:
    return service.create_territory(db, data)


@router.get("", response_model=list[TerritoryRead])
def list_territories(
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> list[TerritoryRead]:
    return service.list_territories(db, limit=limit, offset=offset)


@router.get("/intersects", response_model=list[TerritoryRead])
def list_intersecting_territories(
    wkt: str,
    limit: int = Query(default=100, ge=1, le=1000),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> list[TerritoryRead]:
    return service.list_intersecting_territories(db, wkt=wkt, limit=limit, offset=offset)


@router.get("/{territory_id}", response_model=TerritoryRead)
def get_territory(
    territory_id: int,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> TerritoryRead:
    return service.get_territory(db, territory_id)


@router.patch("/{territory_id}", response_model=TerritoryRead)
def update_territory(
    territory_id: int,
    data: TerritoryUpdate,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> TerritoryRead:
    return service.update_territory(db, territory_id, data)


@router.delete("/{territory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_territory(
    territory_id: int,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> Response:
    service.delete_territory(db, territory_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/{territory_id}/metrics",
    response_model=TerritoryMetricRead,
    status_code=status.HTTP_201_CREATED,
)
def create_metric(
    territory_id: int,
    data: TerritoryMetricCreate,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> TerritoryMetricRead:
    service.get_territory(db, territory_id)
    return service.create_metric(db, territory_id, data)


@router.get("/{territory_id}/metrics", response_model=list[TerritoryMetricRead])
def list_metrics_by_territory(
    territory_id: int,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> list[TerritoryMetricRead]:
    service.get_territory(db, territory_id)
    return service.list_metrics_by_territory(db, territory_id)


@router.patch("/{territory_id}/metrics/{metric_id}", response_model=TerritoryMetricRead)
def update_metric(
    territory_id: int,
    metric_id: int,
    data: TerritoryMetricUpdate,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> TerritoryMetricRead:
    service.get_territory(db, territory_id)
    return service.update_metric(db, territory_id, metric_id, data)


@router.delete("/{territory_id}/metrics/{metric_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_metric(
    territory_id: int,
    metric_id: int,
    db: Session = Depends(get_db),
    service: TerritoryService = Depends(get_territory_service),
) -> Response:
    service.get_territory(db, territory_id)
    service.delete_metric(db, territory_id, metric_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
