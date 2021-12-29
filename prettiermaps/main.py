from osmnx.geometries import geometries_from_polygon
import geopandas as gpd

from prettiermaps import geo
from prettiermaps import plotting
from prettiermaps import prep

LANDCOVER = {
    "urban": {"building": True, "landuse": ["construction"]},
    "water": {"natural": ["water", "bay"]},
    "woodland": {"landuse": ["forest"]},
    "grassland": {
        "landuse": ["grass"],
        "natural": ["island", "wood"],
        "leisure": ["park"],
    },
    "streets": {
        "highway": [
            "motorway",
            "trunk",
            "primary",
            "secondary",
            "tertiary",
            "residential",
            "service",
            "unclassified",
            "pedestrian",
            "footway",
        ]
    },
    "parking": {"amenity": ["parking"], "man_made": ["pier"]},
}

DRAW_SETTINGS = {
    "urban": {
        "cmap": ["#FFC857", "#E9724C", "#C5283D"],
        "ec": "#2F3737",
        "lw": 0.5,
        "zorder": 4,
    },
    "water": {
        "fc": "#a1e3ff",
        "ec": "#2F3737",
        "hatch": "ooo...",
        "lw": 1,
        "zorder": 2,
    },  #'hatch_c': '#85c9e6',
    "grassland": {"fc": "#D0F1BF", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "woodland": {"fc": "#64B96A", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "streets": {"fc": "#2F3737", "ec": "#475657", "alpha": 1, "lw": 0, "zorder": 3},
    "parking": {"fc": "#F2F4CB", "ec": "#2F3737", "lw": 1, "zorder": 3},
}


def main():
    address = "Praça Ferreira do Amaral, Macau"
    radius = 1100

    # aoi = bbox_to_poly(*bbox_from_point(geocode(query=address), dist=radius)) # Might be faster
    aoi = geo.get_aoi_from_user_input(address=address, radius=radius)

    osm_tags = {}
    for element in LANDCOVER.values():
        for k, v in element.items():
            try:
                osm_tags.setdefault(k, []).extend(v)
            except TypeError:
                osm_tags[k] = v

    # TODO: Maybe independent queries that merge together, parallelized.
    # Or define all elements in query, and then
    df = geometries_from_polygon(polygon=aoi, tags=osm_tags)
    df = gpd.clip(df, aoi)

    df = prep.cleanup_df(df=df, landcover=LANDCOVER)
    df = geo.adjust_street_width(df=df)

    # df = df.dissolve(by="osm_type")

    ax = plotting.plot(df, drawing_kwargs=DRAW_SETTINGS)
    return ax
