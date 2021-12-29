from osmnx.geometries import geometries_from_polygon
import geopandas as gpd

from prettiermaps import geo
from prettiermaps import plotting
from prettiermaps import prep

TAGS = {
    "building": True,
    # "landuse": True,
    # "water": True,
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
    ],
}

DRAWING_KWARGS = {
    "background": {"fc": "#F2F4CB", "ec": "#dadbc1", "hatch": "ooo...", "zorder": -1},
    "perimeter": {
        "fc": "#F2F4CB",
        "ec": "#dadbc1",
        "lw": 0,
        "hatch": "ooo...",
        "zorder": 0,
    },
    "green": {"fc": "#D0F1BF", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "forest": {"fc": "#64B96A", "ec": "#2F3737", "lw": 1, "zorder": 1},
    "water": {
        "fc": "#a1e3ff",
        "ec": "#2F3737",
        "hatch": "ooo...",
        "hatch_c": "#85c9e6",
        "lw": 1,
        "zorder": 2,
    },
    "parking": {"fc": "#F2F4CB", "ec": "#2F3737", "lw": 1, "zorder": 3},
    "highway": {"fc": "#2F3737", "ec": "#475657", "alpha": 1, "lw": 0, "zorder": 3},
    "building": {
        "cmap": ["#FFC857", "#E9724C", "#C5283D"],
        "ec": "#2F3737",
        "lw": 0.5,
        "zorder": 4,
    },
}


def main():
    address = "Praça Ferreira do Amaral, Macau"
    radius = 1100

    aoi = geo.get_aoi_from_user_input(address=address, radius=radius)
    # aoi = bbox_to_poly(*bbox_from_point(geocode(query=address), dist=radius)) # Might be faster
    df = geometries_from_polygon(polygon=aoi, tags=TAGS)

    df = prep.cleanup_df(df=df, tags=TAGS)
    df = geo.adjust_street_width(df=df)
    df = gpd.clip(df, aoi)

    # df = df.dissolve(by="osm_type")

    ax = plotting.plot(df, drawing_kwargs=DRAWING_KWARGS)
    return ax
