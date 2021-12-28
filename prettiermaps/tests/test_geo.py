from prettiermaps import geo
from shapely.geometry import Polygon
import pytest


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
    poly = geo.get_aoi_from_user_input(coordinates=(-89.3, 178.2))
    assert isinstance(poly, Polygon)
