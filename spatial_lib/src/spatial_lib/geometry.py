def calculate_area(coords):
    """Calculation of the polygon area by coordinates"""
    from shapely.geometry import Polygon

    return Polygon(coords).area


def centroid(coords):
    """Centroid of the polygon"""
    from shapely.geometry import Polygon

    return Polygon(coords).centroid
