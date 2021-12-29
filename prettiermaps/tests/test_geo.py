from pathlib import Path
import pickle

from mock import patch
import pytest
from shapely.geometry import Polygon, Point
from geopandas import GeoDataFrame
import osmnx as ox

from prettiermaps import geo


def test_validate_coordinates():
    geo.validate_coordinates(lat=-89.3, lon=178.2)
    geo.validate_coordinates(lat=89.3, lon=-178.2)
    with pytest.raises(ValueError):
        geo.validate_coordinates(lat=-92.3, lon=237.2)
    with pytest.raises(ValueError):
        geo.validate_coordinates(lat=92.3, lon=-237.2)


@patch.object(ox, "geocode")
def test_get_aoi_from_user_input(ox_geocode):
    ox_geocode.return_value = 52.52, 13.4

    poly = geo.get_aoi_from_user_input("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.398526785769196,
        52.51910133455738,
        13.40147321595619,
        52.52089866529106,
    )

    poly = geo.get_aoi_from_user_input(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.398526785769196,
        52.51910133455738,
        13.40147321595619,
        52.52089866529106,
    )


@pytest.mark.live
def test_get_aoi_from_user_input_live():
    poly = geo.get_aoi_from_user_input("Unter den Linden 37, 10117 Berlin")
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.386879704802922,
        52.515793839178215,
        13.389825896934692,
        52.51759116066997,
    )
    poly = geo.get_aoi_from_user_input(coordinates=(52.52, 13.4))
    assert isinstance(poly, Polygon)
    assert poly.bounds == (
        13.398526785769196,
        52.51910133455738,
        13.40147321595619,
        52.52089866529106,
    )


def test_adjust_street_width():
    _location_ = Path(__file__).resolve().parent
    with open(_location_ / "mock_data/df_pre_adjusting.pickle", "rb") as handle:
        streets_df = pickle.load(handle)

    streets_df_adjusted = geo.adjust_street_width(streets_df)

    isinstance(streets_df_adjusted, GeoDataFrame)
    assert not all(streets_df_adjusted.is_empty)
    assert streets_df_adjusted.iloc[0].geometry != streets_df.iloc[0].geometry
