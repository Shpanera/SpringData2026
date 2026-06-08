import geopandas as gpd


def create_buffers(objects_gdf: gpd.GeoDataFrame, radius: float) -> gpd.GeoDataFrame:
    """
    Creates buffer polygons around input geometries.

    Args:
        objects_gdf (gpd.GeoDataFrame): GeoDataFrame with source geometries.
        radius (float): Buffer radius in meters.

    Return:
        gpd.GeoDataFrame: Copy of objects_gdf with buffered geometries.

    Raises:
        ValueError: If radius is negative.
    """
    if radius < 0:
        raise ValueError("radius must be non-negative")

    result_gdf = objects_gdf.copy()
    result_gdf.geometry = result_gdf.geometry.buffer(radius)
    return result_gdf
