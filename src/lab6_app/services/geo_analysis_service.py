import geopandas as gpd
from shapely.geometry import Point, Polygon

from src.lab6_app.schemas.responses import GeoAnalysisResponse
from src.lab6_app.services.runtime_config_service import RuntimeConfigService


class GeoAnalysisService:
    def __init__(self, runtime_service: RuntimeConfigService):
        self.runtime_service = runtime_service

    def _sample_data(self) -> tuple[gpd.GeoDataFrame, gpd.GeoDataFrame]:
        districts = gpd.GeoDataFrame(
            {"id": [1, 2]},
            geometry=[
                Polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)]),
                Polygon([(1000, 0), (2000, 0), (2000, 1000), (1000, 1000)]),
            ],
            crs="EPSG:3857",
        )
        objects = gpd.GeoDataFrame(
            {"id": [1, 2]},
            geometry=[Point(500, 500), Point(1500, 500)],
            crs="EPSG:3857",
        )
        return districts, objects

    def coverage_ratio(self) -> GeoAnalysisResponse:
        from buffer_coverage.services.analysis import coverage_ratio

        runtime_cfg = self.runtime_service.get_config()
        districts, objects = self._sample_data()
        result = coverage_ratio(districts, objects, runtime_cfg.default_buffer_radius)
        return GeoAnalysisResponse(
            metric="coverage_ratio",
            radius=runtime_cfg.default_buffer_radius,
            district_count=len(result),
            values=[float(v) for v in result["coverage_ratio"].tolist()],
        )

    def coverage_area(self) -> GeoAnalysisResponse:
        from buffer_coverage.services.analysis import coverage_area

        runtime_cfg = self.runtime_service.get_config()
        districts, objects = self._sample_data()
        result = coverage_area(districts, objects, runtime_cfg.default_buffer_radius)
        return GeoAnalysisResponse(
            metric="coverage_area",
            radius=runtime_cfg.default_buffer_radius,
            district_count=len(result),
            values=[float(v) for v in result["coverage_area"].tolist()],
        )
