from typing import Tuple

import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon, Point


def query_osm_data(aoi: Polygon, custom_filter=None) -> gpd.GeoDataFrame:
    """

    Args:

            custom_filters:Passthrough from osmnx. Filters specific subtypes of e.g. street. Example:
                    '["highway"~"motorway|trunk|primary|secondary|tertiary|residential|service|unclassified|pedestrian|footway"]'

    Returns:

    """
    graph = ox.graph_from_polygon(
        aoi, network_type="all", custom_filter=custom_filter, truncate_by_edge=True
    )
    df = ox.graph_to_gdfs(graph, nodes=False)
    return df


def adjust_street_geometries():
    pass
    # Adjust element width
    # streets_width = {
    # 	'motorway': 5,
    # 	'trunk': 5,
    # 	'primary': 4.5,
    # 	'secondary': 4,
    # 	'tertiary': 3.5,
    # 	'residential': 3,
    # 	'service': 2,
    # 	'unclassified': 2,
    # 	'pedestrian': 2,
    # 	'footway': 1,
    # }
