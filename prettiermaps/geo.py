from typing import Tuple, Optional

import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon, Point
import pandas as pd


def validate_coordinates(lat, lon):
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        raise ValueError(
            "longitude (-90 to 90) and latitude (-180 to 180) coordinates "
            "are not within valid ranges."
        )


def get_aoi_from_user_input(
    address: Optional[str] = None,
    coordinates: Optional[Tuple[float, float]] = None,
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
        lat, lon = coordinates  # type: ignore
    validate_coordinates(lat, lon)

    # buffer in meter
    df = gpd.GeoDataFrame(
        pd.DataFrame([0], columns=["id"]), crs="EPSG:4326", geometry=[Point(lat, lon)]
    )
    df = df.to_crs(df.estimate_utm_crs())
    df.geometry = df.geometry.buffer(radius)
    poly = df.iloc[0].geometry
    return poly


def query_osm_data(aoi: Polygon, custom_filter=None) -> gpd.GeoDataFrame:
    """
    Query OSM data for aoi.

    Args:
        custom_filters:Passthrough from osmnx. Filters specific subtypes of e.g. street. Example:
                '["highway"~"motorway|trunk|primary|secondary|tertiary|residential
                |service|unclassified|pedestrian|footway"]'

    Returns:
        GeodataFrame
    """
    graph = ox.graph_from_polygon(
        aoi, network_type="all", custom_filter=custom_filter, truncate_by_edge=True
    )
    df = ox.graph_to_gdfs(graph, nodes=False)
    return df
