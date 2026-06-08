import geopandas as gpd
import pytest
from shapely.geometry import Point, Polygon

from buffer_coverage.exceptions import CRSMismatchError, EmptyDataError
from buffer_coverage.services.analysis import coverage_area, coverage_ratio, uncovered_areas


@pytest.fixture
def districts_gdf():
    poly = Polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)])
    return gpd.GeoDataFrame({"id": [1]}, geometry=[poly], crs="EPSG:3857")


@pytest.fixture
def objects_gdf():
    pt = Point(500, 500)
    return gpd.GeoDataFrame({"id": [1]}, geometry=[pt], crs="EPSG:3857")


def test_coverage_area_adds_column(districts_gdf, objects_gdf):
    result = coverage_area(districts_gdf, objects_gdf, 200)
    assert "coverage_area" in result.columns
    assert result.loc[0, "coverage_area"] > 0


def test_coverage_ratio_range(districts_gdf, objects_gdf):
    result = coverage_ratio(districts_gdf, objects_gdf, 200)
    value = result.loc[0, "coverage_ratio"]
    assert 0 <= value <= 1


def test_uncovered_areas_not_empty(districts_gdf, objects_gdf):
    result = uncovered_areas(districts_gdf, objects_gdf, 200)
    assert not result.empty
    assert result.geometry.iloc[0].area < districts_gdf.geometry.iloc[0].area


def test_empty_districts_raises(objects_gdf):
    empty = gpd.GeoDataFrame(geometry=[], crs="EPSG:3857")
    with pytest.raises(EmptyDataError):
        coverage_area(empty, objects_gdf, 100)


def test_crs_mismatch_raises(districts_gdf, objects_gdf):
    objects_other = objects_gdf.to_crs("EPSG:4326")
    with pytest.raises(CRSMismatchError):
        coverage_ratio(districts_gdf, objects_other, 100)
