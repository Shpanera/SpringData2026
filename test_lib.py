import geopandas as gpd
from shapely.geometry import Point, Polygon

from src.buffer_coverage import coverage_area, coverage_ratio, uncovered_areas

# Район
districts = gpd.GeoDataFrame(
    geometry=[Polygon([(0, 0), (10000, 0), (10000, 10000), (0, 10000)])],
    crs="EPSG:3857",  # Метрическая проекция
)

# 3 точки
objects = gpd.GeoDataFrame(
    geometry=[
        Point(2500, 5000),  # точка слева
        Point(5000, 5000),  # точка в центре
        Point(7500, 5000),  # точка справа
    ],
    crs="EPSG:3857",
)
radius = 1000

print("Тест coverage_ratio:")
result_ratio = coverage_ratio(districts, objects, radius)
print(f"coverage_ratio: {result_ratio['coverage_ratio'].iloc[0]:.4f}")
print()

print("Тест uncovered_areas:")
result_uncovered = uncovered_areas(districts, objects, radius)
print(f"Количество uncovered областей: {len(result_uncovered)}")
print(f"Есть ли полностью непокрытые области? {result_uncovered.empty}")
print()

print("Тест coverage_area:")
result_area = coverage_area(districts, objects, radius)
print(f"coverage_area: {result_area['coverage_area'].iloc[0]:.2f} кв.м")
print()
