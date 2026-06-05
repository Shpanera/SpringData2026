import geopandas as gpd

from ..exceptions import CRSMismatchError, EmptyDataError, InvalidCRSError


def check_not_empty(gdf: gpd.GeoDataFrame, name: str = "GeoDataFrame") -> None:
    """
    Checks that GeoDataFrame isn't empty.
    Args:
        gdf: GeoDataFrame for validation
        name: of object for the error message (Default is "GeoDataFrame")
    Raises:
        EmptyDataError: If GeoDataFrame is None or empty
    """

    if gdf is None or len(gdf) == 0:
        raise EmptyDataError(f"{name} не должен быть пустым")


def check_crs(gdf: gpd.GeoDataFrame, name: str = "GeoDataFrame") -> None:
    """
     Checks that the GeoDataFrame has a specified coordinate system (CRS).

    Args:
        gdf: GeoDataFrame for validation
        name: of object for the error message (Default is "GeoDataFrame")

    Raises:
        InvalidCRSError: If the GeoDataFrame has no CRS set (crs = None)
    """

    if gdf.crs is None:
        raise InvalidCRSError(f"{name} не имеет заданной CRS")


def check_same_crs(gdf1: gpd.GeoDataFrame, gdf2: gpd.GeoDataFrame) -> None:
    """
    Checks if the coordinate systems of two GeoDataFrame match
      Args:
        gdf1: The first GeoDataFrame to check
        gdf2: Second GeoDataFrame to check

    Raises:
        CRSMismatchError: If the CRS of the GeoDataFrame do not match
    """
    check_crs(gdf1, "gdf1")
    check_crs(gdf2, "gdf2")

    if gdf1.crs != gdf2.crs:
        raise CRSMismatchError(f"CRS не совпадают: {gdf1.crs} и {gdf2.crs}")
