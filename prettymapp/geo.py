from typing import Tuple, Optional

from osmnx.geocoder import geocode
from geopandas import GeoDataFrame
import pandas as pd
from pandas import DataFrame
from shapely.geometry import Polygon, Point, box


class GeoCodingError(Exception):
    pass


def validate_coordinates(lat: float, lon: float) -> None:
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        raise ValueError(
            "longitude (-90 to 90) and latitude (-180 to 180) coordinates "
            "are not within valid ranges."
        )


def get_aoi(
    address: Optional[str] = None,
    coordinates: Optional[Tuple[float, float]] = None,
    radius: int = 1000,
    rectangular: bool = False,
) -> Polygon:
    """
    Gets round or rectangular shapely Polygon in in 4326 from input address or coordinates.

    Args:
        address: Address string
        coordinates: lat, lon
        radius: Radius in meter
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
        try:
            lat, lon = geocode(address)
        except ValueError as e:
            raise GeoCodingError(f"Could not geocode address '{address}'") from e
    else:
        lat, lon = coordinates  # type: ignore
    validate_coordinates(lat, lon)

    df = GeoDataFrame(
        DataFrame([0], columns=["id"]), crs="EPSG:4326", geometry=[Point(lon, lat)]
    )
    utm_crs = df.estimate_utm_crs()
    df = df.to_crs(utm_crs)
    df.geometry = df.geometry.buffer(radius)
    df = df.to_crs(crs=4326)
    poly = df.iloc[0].geometry

    if rectangular:
        poly = box(*poly.bounds)

    return poly


def explode_multigeometries(df: GeoDataFrame) -> GeoDataFrame:
    """
    Explode all multi geometries in a geodataframe into individual polygon geometries.
    Adds exploded polygons as rows at the end of the geodataframe and resets its index.
    Args:
        df: Input GeoDataFrame
    """
    mask = df.geom_type.isin(["MultiPolygon", "MultiLineString", "MultiPoint"])
    outdf = df[~mask]
    df_multi = df[mask]
    for _, row in df_multi.iterrows():
        df_temp = GeoDataFrame(
            pd.DataFrame.from_records([row.to_dict()] * len(row.geometry.geoms)), crs="EPSG:4326"
        )
        df_temp.geometry = list(row.geometry.geoms)
        outdf = GeoDataFrame(pd.concat([outdf, df_temp], ignore_index=True), crs="EPSG:4326")

    outdf = outdf.reset_index(drop=True)
    return outdf
