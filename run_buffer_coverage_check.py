import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent / "src"))

import geopandas as gpd
from shapely.geometry import Point, Polygon

from buffer_coverage.services.analysis import coverage_area, coverage_ratio, uncovered_areas


def main() -> None:
    districts = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[Polygon([(0, 0), (1000, 0), (1000, 1000), (0, 1000)])],
        crs="EPSG:3857",
    )

    objects = gpd.GeoDataFrame(
        {"id": [1]},
        geometry=[Point(500, 500)],
        crs="EPSG:3857",
    )

    area_result = coverage_area(districts, objects, 200)
    ratio_result = coverage_ratio(districts, objects, 200)
    uncovered_result = uncovered_areas(districts, objects, 200)

    print("Coverage area result:")
    print(area_result[["id", "coverage_area"]])
    print()

    print("Coverage ratio result:")
    print(ratio_result[["id", "coverage_ratio"]])
    print()

    print("Uncovered areas result:")
    print(uncovered_result)
    print()

    print("Done: buffer_coverage works on the sample data.")


if __name__ == "__main__":
    main()
