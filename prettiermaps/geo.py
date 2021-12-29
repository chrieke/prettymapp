from typing import Tuple, Optional

import osmnx as ox
from geopandas import GeoDataFrame
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
    df = GeoDataFrame(
        pd.DataFrame([0], columns=["id"]), crs="EPSG:4326", geometry=[Point(lon, lat)]
    )
    df = df.to_crs(df.estimate_utm_crs())
    df.geometry = df.geometry.buffer(radius)
    df = df.to_crs(crs=4326)
    poly = df.iloc[0].geometry
    return poly


def query_osm_streets(
    aoi: Polygon,
    custom_filter='["highway"~"motorway|trunk|primary|secondary|tertiary|'
    'residential|service|unclassified|pedestrian|footway"]',
) -> GeoDataFrame:
    """
    Query OSM data for aoi.

    Args:
        custom_filters:Passthrough from osmnx. Filters specific subtypes of e.g. street. Example:
                '["highway"~"motorway|trunk|primary|secondary|tertiary|residential
                |service|unclassified|pedestrian|footway"]'

    Returns:
        GeodataFrame
    """
    # TODO: Make custom filter selectable via templates etc.?
    graph = ox.graph_from_polygon(
        aoi, network_type="all", custom_filter=custom_filter, truncate_by_edge=True
    )
    graph = ox.project_graph(graph)  # UTM  #TODO: Check if faster with geopandas
    df = ox.graph_to_gdfs(graph, nodes=False)
    # TODO: Intersection with aoi circle?
    return df


def adjust_street_width(df_streets: GeoDataFrame) -> GeoDataFrame:
    """
    Adjusts the street Linestrings to thicker Polygons (better visible when plotted).

    Args:
        df_streets: Geodataframe with street linestrings.

    Returns:
        Geodataframe with street Polygons
    """
    # TODO: As parameters?
    streets_width = {
        "motorway": 5,
        "trunk": 5,
        "primary": 4.5,
        "primary_link": 4.5,
        "secondary": 4,
        "secondary_link": 4,
        "tertiary": 3.5,
        "tertiary_link": 3.5,
        "residential": 3,
        "service": 2,
        "unclassified": 2,
        "pedestrian": 2,
        "footway": 1,
    }

    def _dilate(row):
        try:
            dilation = streets_width[row["highway"]]
        except TypeError:
            dilation = streets_width[row["highway"][0]]
        row.geometry = row.geometry.buffer(dilation)
        return row

    df_streets_adjusted = df_streets.apply(_dilate, axis=1)
    return df_streets_adjusted
