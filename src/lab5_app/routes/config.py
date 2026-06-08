from fastapi import APIRouter, Request

from ..config import AppConfig, RuntimeConfig
from ..services.runtime_config import RuntimeConfigService

router = APIRouter(prefix="/config", tags=["config"])


@router.get("/app", response_model=AppConfig)
def get_app_config(request: Request) -> AppConfig:
    return request.app.state.startup_config


@router.get("/runtime", response_model=RuntimeConfig)
def get_runtime_config(request: Request) -> RuntimeConfig:
    service: RuntimeConfigService = request.app.state.runtime_config_service
    return service.get()


@router.put("/runtime", response_model=RuntimeConfig)
def update_runtime_config(request: Request, payload: RuntimeConfig) -> RuntimeConfig:
    service: RuntimeConfigService = request.app.state.runtime_config_service
    return service.update(payload)
