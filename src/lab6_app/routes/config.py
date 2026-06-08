from fastapi import APIRouter, Depends

from src.lab6_app.dependencies import get_app_config, get_runtime_config_service
from src.lab6_app.schemas.app_config import AppConfigModel
from src.lab6_app.schemas.responses import HealthResponse
from src.lab6_app.schemas.runtime_config import RuntimeConfigModel, RuntimeConfigUpdateModel
from src.lab6_app.services.runtime_config_service import RuntimeConfigService

router = APIRouter(tags=["configuration"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@router.get("/config/app", response_model=AppConfigModel)
def read_app_config(app_config: AppConfigModel = Depends(get_app_config)) -> AppConfigModel:
    return app_config


@router.get("/config/runtime", response_model=RuntimeConfigModel)
def read_runtime_config(
    runtime_service: RuntimeConfigService = Depends(get_runtime_config_service),
) -> RuntimeConfigModel:
    return runtime_service.get_config()


@router.put("/config/runtime", response_model=RuntimeConfigModel)
def update_runtime_config(
    payload: RuntimeConfigUpdateModel,
    runtime_service: RuntimeConfigService = Depends(get_runtime_config_service),
) -> RuntimeConfigModel:
    return runtime_service.update_config(payload)
