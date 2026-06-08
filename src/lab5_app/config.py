from __future__ import annotations

import os
from functools import lru_cache
from typing import List

from pydantic import BaseModel, Field, field_validator


class AppConfig(BaseModel):
    app_name: str = Field(default="Laboratory FastAPI App")
    app_version: str = Field(default="1.0.0")
    app_description: str = Field(default="Учебное приложение")
    app_authors: List[str] = Field(default_factory=lambda: ["VikaRatmanova"])
    contact_email: str | None = Field(default=None)
    license_name: str | None = Field(default=None)

    @classmethod
    def from_env(cls) -> "AppConfig":
        raw_authors = os.getenv("APP_AUTHORS", "VikaRatmanova")
        authors = [item.strip() for item in raw_authors.split(",") if item.strip()]
        return cls(
            app_name=os.getenv("APP_NAME", "Laboratory FastAPI App"),
            app_version=os.getenv("APP_VERSION", "1.0.0"),
            app_description=os.getenv("APP_DESCRIPTION", "Учебное приложение"),
            app_authors=authors,
            contact_email=os.getenv("CONTACT_EMAIL"),
            license_name=os.getenv("LICENSE_NAME"),
        )


class RuntimeConfig(BaseModel):
    log_level: str = Field(default="INFO")
    feature_flag: bool = Field(default=False)
    maintenance_mode: bool = Field(default=False)
    runtime_message: str = Field(default="Сервис работает в стандартном режиме")

    @field_validator("log_level")
    @classmethod
    def validate_log_level(cls, value: str) -> str:
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        upper = value.upper()
        if upper not in allowed:
            raise ValueError(f"log_level must be one of: {', '.join(sorted(allowed))}")
        return upper

    @classmethod
    def from_env(cls) -> "RuntimeConfig":
        return cls(
            log_level=os.getenv("RUNTIME_LOG_LEVEL", "INFO"),
            feature_flag=os.getenv("FEATURE_FLAG", "false").lower() == "true",
            maintenance_mode=os.getenv("MAINTENANCE_MODE", "false").lower() == "true",
            runtime_message=os.getenv(
                "RUNTIME_MESSAGE", "Сервис работает в стандартном режиме"
            ),
        )


@lru_cache(maxsize=1)
def get_startup_config() -> AppConfig:
    return AppConfig.from_env()
