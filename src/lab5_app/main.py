from fastapi import FastAPI

from .config import RuntimeConfig, get_startup_config
from .routes.config import router as config_router
from .routes.health import router as health_router
from .services.runtime_config import RuntimeConfigService

startup_config = get_startup_config()

app = FastAPI(
    title=startup_config.app_name,
    version=startup_config.app_version,
    description=startup_config.app_description,
)

app.state.startup_config = startup_config
app.state.runtime_config_service = RuntimeConfigService(RuntimeConfig.from_env())

app.include_router(health_router)
app.include_router(config_router)
