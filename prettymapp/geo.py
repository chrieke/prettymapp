import osmnx as ox
from geopandas import GeoDataFrame
from pandas import DataFrame
from shapely.geometry import Polygon, Point, box


class GeoCodingError(Exception):
    pass


def validate_coordinates(lat: float, lon: float) -> None:
    if lat < -90 or lat > 90 or lon < -180 or lon > 180:
        raise ValueError(
            "latitude (-90 to 90) and longitude (-180 to 180) coordinates "
            "are not within valid ranges."
        )


def get_aoi(
    address: str | None = None,
    coordinates: tuple[float, float] | None = None,
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
        if not address.strip():
            raise GeoCodingError("No address provided, please enter a location.")
        try:
            lat, lon = ox.geocode(address)
        except ValueError as e:
            raise GeoCodingError(f"Could not geocode address '{address}'") from e
        except Exception as e:  # pylint: disable=broad-except
            # osmnx/requests surface network, timeout and HTTP errors as a range of
            # exception types; treat them all as a transient geocoding failure.
            raise GeoCodingError(
                f"Could not reach the geocoding service while looking up "
                f"'{address}'. Please try again."
            ) from e
    else:
        if coordinates is None:
            raise ValueError("Either 'address' or 'coordinates' must be provided.")
        lat, lon = coordinates
    validate_coordinates(lat, lon)

    df = GeoDataFrame(
        DataFrame([0], columns=["id"]), crs="EPSG:4326", geometry=[Point(lon, lat)]
    )
    df = df.to_crs(df.estimate_utm_crs())
    df.geometry = df.geometry.buffer(radius)
    df = df.to_crs(crs=4326)
    poly = df.iloc[0].geometry

    if rectangular:
        poly = box(*poly.bounds)

    return poly


def explode_multigeometries(df: GeoDataFrame) -> GeoDataFrame:
    """
    Explode all multi-part geometries in a geodataframe into individual
    single-part geometries, one row each, and reset the index.

    Args:
        df: Input GeoDataFrame
    """
    return df.explode(index_parts=False).reset_index(drop=True)
