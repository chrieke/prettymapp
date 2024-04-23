from prettymapp.osm import get_osm_tags, get_osm_geometries_from_xml


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
    filepath = "./mock_data/osm_export_xml.osm"
    df = get_osm_geometries_from_xml(filepath)
    assert df.shape == (18, 3)
