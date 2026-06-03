from src.lab6_app.common.config import RuntimeConfig, StartupConfig
from src.lab6_app.services.geo_analysis_service import GeoAnalysisService
from src.lab6_app.services.runtime_config_service import RuntimeConfigService


class DependencyContainer(dict):
    def get_required(self, key: str):
        if key not in self:
            raise KeyError(f"Dependency '{key}' not found")
        return self[key]


def init_dependencies() -> DependencyContainer:
    startup_config = StartupConfig.from_env()
    runtime_model = RuntimeConfig.from_env().to_model()
    runtime_service = RuntimeConfigService(runtime_model)

    container = DependencyContainer()
    container["app_config"] = startup_config.to_model()
    container["runtime_config_service"] = runtime_service
    container["geo_analysis_service"] = GeoAnalysisService(runtime_service)
    return container
