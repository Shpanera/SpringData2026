import os
from dataclasses import dataclass, field

from src.lab6_app.schemas.app_config import AppConfigModel
from src.lab6_app.schemas.runtime_config import RuntimeConfigModel


@dataclass(frozen=True)
class StartupConfig:
    app_name: str
    app_version: str
    app_description: str
    app_authors: list[str] = field(default_factory=list)
    contact_email: str | None = None
    license_name: str | None = None

    @classmethod
    def from_env(cls) -> "StartupConfig":
        raw_authors = os.getenv("APP_AUTHORS", "Михаил Выстрчил")
        authors = [item.strip() for item in raw_authors.split(",") if item.strip()]
        return cls(
            app_name=os.getenv("APP_NAME", "Laboratory FastAPI App"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            app_description=os.getenv(
                "APP_DESCRIPTION", "Учебное приложение на FastAPI"
            ),
            app_authors=authors,
            contact_email=os.getenv("CONTACT_EMAIL"),
            license_name=os.getenv("LICENSE_NAME"),
        )

    def to_model(self) -> AppConfigModel:
        return AppConfigModel(
            app_name=self.app_name,
            app_version=self.app_version,
            app_description=self.app_description,
            app_authors=self.app_authors,
            contact_email=self.contact_email,
            license_name=self.license_name,
        )


@dataclass
class RuntimeConfig:
    log_level: str = "INFO"
    feature_flag: bool = False
    maintenance_mode: bool = False
    runtime_message: str = "Приложение работает в штатном режиме"
    default_buffer_radius: float = 200.0

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        return cls(
            log_level=os.getenv("RUNTIME_LOG_LEVEL", "INFO"),
            feature_flag=os.getenv("FEATURE_FLAG", "false").lower() == "true",
            maintenance_mode=os.getenv("MAINTENANCE_MODE", "false").lower() == "true",
            runtime_message=os.getenv(
                "RUNTIME_MESSAGE", "Приложение работает в штатном режиме"
            ),
            default_buffer_radius=float(os.getenv("DEFAULT_BUFFER_RADIUS", "200")),
        )

    def to_model(self) -> RuntimeConfigModel:
        return RuntimeConfigModel(
            log_level=self.log_level,
            feature_flag=self.feature_flag,
            maintenance_mode=self.maintenance_mode,
            runtime_message=self.runtime_message,
            default_buffer_radius=self.default_buffer_radius,
        )
