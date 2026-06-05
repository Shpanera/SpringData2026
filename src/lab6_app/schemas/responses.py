from typing import Literal

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: Literal["ok"] = "ok"


class GeoAnalysisResponse(BaseModel):
    metric: str
    radius: float
    district_count: int
    values: list[float] = Field(default_factory=list)
