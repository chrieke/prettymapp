from osmnx.geometries import geometries_from_polygon
import geopandas as gpd

from prettiermaps import geo
from prettiermaps import plotting
from prettiermaps import prep

TAGS = {
    "building": True,
    # "landuse": True,
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


def main():
    address = "Praça Ferreira do Amaral, Macau"
    radius = 1100

    aoi = geo.get_aoi_from_user_input(address=address, radius=radius)
    # aoi = bbox_to_poly(*bbox_from_point(geocode(query=address), dist=radius)) # Might be faster
    df = geometries_from_polygon(polygon=aoi, tags=TAGS)

    df = prep.cleanup_df(df=df, tags=TAGS)
    df = geo.adjust_street_width(df=df)
    df = gpd.clip(df, aoi)

    # TODO: Noch net hier weil gebäude andere farben geplottet.
    df = df.dissolve(by="osm_type")

    plotting.plot(df, aoi)
    return df
