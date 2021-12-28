import pytest
from shapely.geometry import Polygon
from geopandas import GeoDataFrame
from shapely.geometry import Point

from prettiermaps import geo


def test_validate_coordinates():
    geo.validate_coordinates(lat=-89.3, lon=178.2)
    geo.validate_coordinates(lat=89.3, lon=-178.2)
    with pytest.raises(ValueError):
        geo.validate_coordinates(lat=-92.3, lon=237.2)
    with pytest.raises(ValueError):
        geo.validate_coordinates(lat=92.3, lon=-237.2)


def test_get_aoi_from_user_input():
    poly = geo.get_aoi_from_user_input("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    poly = geo.get_aoi_from_user_input(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)


def test_query_osm_data():
    aoi = Point(13.380972146987915, 52.51517622886228).buffer(0.001)
    df = geo.query_osm_data(aoi=aoi)
    isinstance(df, GeoDataFrame)
    assert not all(df.is_empty)
