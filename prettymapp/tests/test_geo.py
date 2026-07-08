from mock import patch
import pytest
from shapely.geometry import Polygon, MultiPolygon
import geopandas as gpd
import pandas as pd

from prettymapp.geo import (
    validate_coordinates,
    get_aoi,
    GeoCodingError,
    explode_multigeometries,
)


def test_validate_coordinates():
    validate_coordinates(lat=-89.3, lon=178.2)
    validate_coordinates(lat=89.3, lon=-178.2)
    with pytest.raises(ValueError):
        validate_coordinates(lat=-92.3, lon=237.2)
    with pytest.raises(ValueError):
        validate_coordinates(lat=92.3, lon=-237.2)


# Patch the name used inside prettymapp.geo (module attribute lookup at call
# time), NOT osmnx directly - `from osmnx import geocode`-style bindings would
# bypass a patch on the osmnx module and silently hit the live geocoder.
@patch("prettymapp.geo.ox.geocode")
def test_get_aoi_from_user_input_address(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi("Unter den Linden 37, 10117 Berlin")
    ox_geocode.assert_called_once()
    assert isinstance(poly, Polygon)
    assert poly.bounds == pytest.approx(
        (
            13.38526793559592,
            52.511013338753465,
            13.414732236942758,
            52.52898664609029,
        )
    )
    assert poly.area == pytest.approx(0.00041546027853784154)


@patch("prettymapp.geo.ox.geocode")
def test_get_aoi_from_user_input_coordinates(ox_geocode):
    poly = get_aoi(coordinates=(52.52, 13.4))
    ox_geocode.assert_not_called()
    assert isinstance(poly, Polygon)
    assert poly.bounds == pytest.approx(
        (
            13.38526793559592,
            52.511013338753465,
            13.414732236942758,
            52.52898664609029,
        )
    )


@patch("prettymapp.geo.ox.geocode")
def test_get_aoi_from_user_input_rectangle(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = get_aoi("Unter den Linden 37, 10117 Berlin", rectangular=True)
    ox_geocode.assert_called_once()
    assert isinstance(poly, Polygon)
    assert poly.bounds == pytest.approx(
        (
            13.38526793559592,
            52.511013338753465,
            13.414732236942758,
            52.52898664609029,
        )
    )
    assert poly.area == pytest.approx(0.0005295709435715184)


@pytest.mark.live
def test_get_aoi_from_user_input_address_live():
    poly = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == pytest.approx(
        (
            13.373621926483281,
            52.507705884952586,
            13.403083847278062,
            52.52567909987013,
        )
    )


@pytest.mark.live
def test_get_aoi_from_user_input_coordinates_live():
    poly = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == pytest.approx(
        (
            13.38526793559592,
            52.51101333875345,
            13.414732236942758,
            52.52898664609028,
        )
    )


@pytest.mark.live
def test_get_aoi_invalid_address_raises():
    with pytest.raises(GeoCodingError):
        get_aoi("not_an_address")


def test_get_aoi_empty_address_raises():
    with pytest.raises(GeoCodingError):
        get_aoi("   ")


@patch("prettymapp.geo.ox.geocode")
def test_get_aoi_geocode_network_error_raises(mock_geocode):
    mock_geocode.side_effect = ConnectionError("boom")
    with pytest.raises(GeoCodingError):
        get_aoi("Unter den Linden 37, 10117 Berlin")


def test_explode_multigeoemtries():
    poly1 = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    poly2 = Polygon([[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]])
    multipoly = MultiPolygon([poly1, poly2])
    df = gpd.GeoDataFrame(
        pd.DataFrame([0, 1], columns=["id"]),
        crs="EPSG:4326",
        geometry=[poly1, multipoly],
    )
    df_result = explode_multigeometries(df)

    assert df.shape[0] != df_result.shape[0]
    assert df_result.shape[0] == 3
