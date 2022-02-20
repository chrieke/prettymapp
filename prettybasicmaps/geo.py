from typing import Tuple, Optional, Any

import streamlit as st
from osmnx.geocoder import geocode
from geopandas import GeoDataFrame
from pandas import DataFrame
from shapely.geometry import Polygon, Point, box


def validate_coordinates(lat: float, lon: float) -> None:
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        raise ValueError(
            "longitude (-90 to 90) and latitude (-180 to 180) coordinates "
            "are not within valid ranges."
        )


# @st.cache()
def get_aoi(
    address: Optional[str] = None,
    coordinates: Optional[Tuple[float, float]] = None,
    distance: int = 1000,
    rectangular: bool = False,
) -> Tuple[Polygon, Any]:
    """
    Gets round or rectangular shapely Polygon in in 4326 from input address or coordinates.

    Args:
        address: Address string
        coordinates: lat, lon
        distance: Radius in meter
        rectangular: Optionally return aoi as rectangular polygon, default False.

    Returns:
        shapely Polygon in 4326 crs
    """
    if address is not None:
        if coordinates is not None:
            raise ValueError(
                "Both address and latlon coordinates were provided, please "
                "select only one!"
            )
        lat, lon = geocode(address)
    else:
        lat, lon = coordinates  # type: ignore
    validate_coordinates(lat, lon)

    df = GeoDataFrame(
        DataFrame([0], columns=["id"]), crs="EPSG:4326", geometry=[Point(lon, lat)]
    )
    utm_crs = df.estimate_utm_crs()
    df = df.to_crs(utm_crs)
    df.geometry = df.geometry.buffer(distance)
    df = df.to_crs(crs=4326)
    poly = df.iloc[0].geometry

    if rectangular:
        poly = box(*poly.bounds)

    return poly, utm_crs


def adjust_street_width(
    df: GeoDataFrame, aoi_utm_crs: Optional[Any] = None
) -> GeoDataFrame:
    """
    Adjusts the street Linestrings to thicker Polygons (better visible when plotted).

    Args:
        df_streets: Geodataframe with street linestrings, requires "street" column.

    Returns:
        Geodataframe with street Polygons
    """
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

    def _find_buffer_strength(row):
        try:
            dilation = streets_width[row["highway"]]
        except TypeError:
            dilation = streets_width[row["highway"][0]]
        return dilation

    if aoi_utm_crs is None:
        aoi_utm_crs = df.estimate_utm_crs()

    df = df.to_crs(aoi_utm_crs)
    df["buffer_strength"] = df.apply(_find_buffer_strength, axis=1)
    df.geometry = df.geometry.buffer(df["buffer_strength"])
    df = df.to_crs(crs=4326)
    return df
