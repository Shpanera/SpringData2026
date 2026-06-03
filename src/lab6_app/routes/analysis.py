from fastapi import APIRouter, Depends

from src.lab6_app.dependencies import get_geo_analysis_service
from src.lab6_app.schemas.responses import GeoAnalysisResponse
from src.lab6_app.services.geo_analysis_service import GeoAnalysisService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.get("/coverage-ratio", response_model=GeoAnalysisResponse)
def get_coverage_ratio(
    service: GeoAnalysisService = Depends(get_geo_analysis_service),
) -> GeoAnalysisResponse:
    return service.coverage_ratio()


@router.get("/coverage-area", response_model=GeoAnalysisResponse)
def get_coverage_area(
    service: GeoAnalysisService = Depends(get_geo_analysis_service),
) -> GeoAnalysisResponse:
    return service.coverage_area()
