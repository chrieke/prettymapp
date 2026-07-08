from pathlib import Path

from mock import patch
import pytest
from geopandas import GeoDataFrame
from shapely.geometry import box

from prettymapp.osm import (
    get_osm_tags,
    get_osm_geometries,
    get_osm_geometries_from_xml,
    cleanup_osm_df,
    InsufficientResponseError,
    OsmDataError,
)


def test_get_osm_tags():
    tags = get_osm_tags()
    assert tags == {
        "building": True,
        "landuse": [
            "construction",
            "commercial",
            "forest",
            "grass",
            "vineyard",
            "orchard",
            "village_green",
        ],
        "natural": ["water", "bay", "island", "wood"],
        "place": ["sea"],
        "leisure": ["swimming_pool", "park", "pitch", "garden", "golf_course"],
        "highway": [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "cycleway",
            "residential",
            "service",
            "unclassified",
            "footway",
            "motorway_link",
            "pedestrian",
        ],
        "railway": True,
        "amenity": ["parking"],
        "man_made": ["pier"],
    }


def test_get_osm_geometries_from_xml():
    filepath = Path(__file__).parent / "mock_data" / "osm_export_xml.osm"
    df = get_osm_geometries_from_xml(filepath)
    assert df.shape == (18, 3)


def test_cleanup_osm_df_empty_input_raises():
    with pytest.raises(OsmDataError):
        cleanup_osm_df(GeoDataFrame())


@patch("prettymapp.osm.ox.features_from_polygon")
def test_get_osm_geometries_no_features_raises(mock_features):
    mock_features.side_effect = InsufficientResponseError("no matching features")
    with pytest.raises(OsmDataError):
        get_osm_geometries(box(0, 0, 0.001, 0.001))
