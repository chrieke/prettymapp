from pathlib import Path
import pickle

from mock import patch
import pytest
from shapely.geometry import Polygon
from geopandas import GeoDataFrame
import osmnx as ox
from prettybasicmaps.geo import validate_coordinates, get_aoi, adjust_street_width


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

    poly, utm_crs = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.373621926483281,
        52.507705884952586,
        13.403083847278062,
        52.52567909987013,
    )
    assert poly.area == 0.00041542753985753027
    assert str(utm_crs) == "epsg:32633"


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_coordinates(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly, utm_crs = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.38526793559592,
        52.51101333875345,
        13.414732236942758,
        52.52898664609028,
    )
    assert str(utm_crs) == "epsg:32633"


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input_rectangle(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly, utm_crs = get_aoi("Unter den Linden 37, 10117 Berlin", rectangular=True)
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.373621926483281,
        52.507705884952586,
        13.403083847278062,
        52.52567909987013,
    )
    assert poly.area == 0.0005295254343283185
    assert str(utm_crs) == "epsg:32633"


@pytest.mark.live
def test_get_aoi_from_user_input_address_live():
    poly, _ = get_aoi("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.373621926483281,
        52.507705884952586,
        13.403083847278062,
        52.52567909987013,
    )


@pytest.mark.live
def test_get_aoi_from_user_input_coordinates_live():
    poly, _ = get_aoi(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.38526793559592,
        52.51101333875345,
        13.414732236942758,
        52.52898664609028,
    )


def test_adjust_street_width():
    _location_ = Path(__file__).resolve().parent
    with open(_location_ / "mock_data/df_pre_adjusting.pickle", "rb") as handle:
        streets_df = pickle.load(handle)

    streets_df_adjusted = adjust_street_width(streets_df)

    isinstance(streets_df_adjusted, GeoDataFrame)
    assert not all(streets_df_adjusted.is_empty)
    assert streets_df_adjusted.iloc[0].geometry != streets_df.iloc[0].geometry
