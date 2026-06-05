from fastapi import Request

from src.lab6_app.schemas.app_config import AppConfigModel
from src.lab6_app.services.geo_analysis_service import GeoAnalysisService
from src.lab6_app.services.runtime_config_service import RuntimeConfigService

from src.lab6_app.services.territory_service import TerritoryService

def get_territory_service(request: Request) -> TerritoryService:
    return request.app.state.dependencies.get_required("territory_service")

def get_system_service(request: Request) -> dict:
    return request.app.state.dependencies


def get_app_config(request: Request) -> AppConfigModel:
    return request.app.state.dependencies.get_required("app_config")


def get_runtime_config_service(request: Request) -> RuntimeConfigService:
    return request.app.state.dependencies.get_required("runtime_config_service")


def get_geo_analysis_service(request: Request) -> GeoAnalysisService:
    return request.app.state.dependencies.get_required("geo_analysis_service")
