from osmnx.geometries import geometries_from_polygon
import geopandas as gpd

from prettybasicmaps import geo
from prettybasicmaps import plotting
from prettybasicmaps import dataclean
from prettybasicmaps.settings import LANDCOVER, DRAW_SETTINGS


def main(address="Praça Ferreira do Amaral, Macau", radius=1100):

    osm_tags = dataclean.osm_tags_from_settings(settings=LANDCOVER)

    # aoi = bbox_to_poly(*bbox_from_point(geocode(query=address), dist=radius)) # Might be faster
    aoi = geo.get_aoi_from_user_input(address=address, radius=radius)

    df = geometries_from_polygon(polygon=aoi, tags=osm_tags)
    df = gpd.clip(df, aoi)

    df = dataclean.cleanup_df(df=df, landcover=LANDCOVER)
    df = geo.adjust_street_width(df=df)

    ax = plotting.plot(df, drawing_kwargs=DRAW_SETTINGS)
    return ax


if __name__ == "__main__":
    ax = main()
    # plt.show()
