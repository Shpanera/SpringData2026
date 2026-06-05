from pydantic import BaseModel, Field


class AppConfigModel(BaseModel):
    app_name: str = Field(default="Laboratory FastAPI App")
    app_version: str = Field(default="1.0.0")
    app_description: str = Field(default="Учебное приложение на FastAPI")
    app_authors: list[str] = Field(default_factory=lambda: ["Михаил Выстрчил"])
    contact_email: str | None = Field(default=None)
    license_name: str | None = Field(default=None)
