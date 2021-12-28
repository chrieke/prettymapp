from typing import Tuple

import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon, Point


def validate_coordinates(lat, lon):
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        raise ValueError(
            "longitude (-90 to 90) and latitude (-180 to 180) coordinates "
            "are not within valid ranges."
        )


def get_aoi_from_user_input(
    address: str = None,
    coordinates: Tuple[float, float] = None,
    radius=100,
) -> Polygon:
    """
    Gets shapely Polygon from input address or coordinates.
    Args:
            address: Address string
            coordinates: lat, lon
            radius: Radius in meter

    Returns:
            shapely Polygon
    """
    if address is not None:
        if coordinates is not None:
            raise ValueError(
                "Both address and latlon coordinates were provided, please "
                "select only one!"
            )
        lat, lon = ox.geocode(address)
    else:
        lat, lon = coordinates
    validate_coordinates(lat, lon)

    poly = Point(lat, lon).buffer(radius)
    return poly
