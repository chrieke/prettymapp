from mock import patch
import pytest
from shapely.geometry import Polygon
import osmnx as ox
from prettymapp.geo import (
    validate_coordinates,
    get_aoi,
    GeoCodingError,
)


def test_validate_coordinates():
    validate_coordinates(lat=-89.3, lon=178.2)
    validate_coordinates(lat=89.3, lon=-178.2)
    with pytest.raises(ValueError):
        validate_coordinates(lat=-92.3, lon=237.2)
    with pytest.raises(ValueError):
        validate_coordinates(lat=92.3, lon=-237.2)


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_address(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.373621926483281,
        52.507705884952586,
        13.403083847278062,
        52.52567909987013,
    )
    assert poly.area == 0.00041542753985753124


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_coordinates(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.38526793559592,
        52.51101333875345,
        13.414732236942758,
        52.52898664609028,
    )


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_rectangle(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi("Unter den Linden 37, 10117 Berlin", rectangular=True)
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.373621926483281,
        52.507705884952586,
        13.403083847278062,
        52.52567909987013,
    )
    assert poly.area == 0.0005295254343283185


@pytest.mark.live
def test_get_aoi_from_user_input_address_live():
    poly = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.373621926483281,
        52.507705884952586,
        13.403083847278062,
        52.52567909987013,
    )


@pytest.mark.live
def test_get_aoi_from_user_input_coordinates_live():
    poly = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.38526793559592,
        52.51101333875345,
        13.414732236942758,
        52.52898664609028,
    )


@pytest.mark.live
def test_get_aoi_invalid_address_raises():
    with pytest.raises(GeoCodingError):
        get_aoi("not_an_address")
