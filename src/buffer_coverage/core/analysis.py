import geopandas as gpd

from ..core.geometry import create_buffers
from ..utils.validators import check_not_empty, check_same_crs


def coverage_ratio(
    districts_gdf: gpd.GeoDataFrame, objects_gdf: gpd.GeoDataFrame, radius: float
) -> float:
    """
    Calculates the fraction for each district covered by the buffers.

    Args:
        districts_gdf (gpd.GeoDataFrame): GeoDataFrame with polygons of districts.
            It must contain geometry in any format (it will be converted to EPSG:3857).
        objects_gdf (gpd.GeoDataFrame): GeoDataFrame with point or polygon
            objects around which buffers are created. Must have the same coordinate system as the districts_gdf.
        radius (float): The radius of the buffer zone in meters.
    Return:
        result_gdf (gpd.GeoDataFrame): A copy of the districts_gdf with the added 'coverage_ratio' column. Number (float) from 0 to 1.
    """
    check_not_empty(districts_gdf, "districts_gdf")
    check_not_empty(objects_gdf, "objects_gdf")
    check_same_crs(districts_gdf, objects_gdf)

    districts = districts_gdf.to_crs(epsg=3857)
    objects = objects_gdf.to_crs(epsg=3857)

    buffers = create_buffers(objects, radius)

    union_buffer = buffers.geometry.union_all()

    intersections = districts.geometry.intersection(union_buffer)
    covered_areas = intersections.area

    total_areas = districts.geometry.area

    coverage_ratios = covered_areas / total_areas
    coverage_ratios[total_areas == 0] = 0.0

    result_gdf = districts_gdf.copy()
    result_gdf["coverage_ratio"] = coverage_ratios

    return result_gdf
