from osmnx.geometries import geometries_from_polygon
from osmnx.utils import config
from geopandas import clip
import pandas as pd

from prettybasicmaps import geo
from prettybasicmaps import plotting
from prettybasicmaps import dataprep
from prettybasicmaps.settings import LC_SETTINGS, DRAW_SETTINGS


# TODO: Activate
config(use_cache=False)


def main(
    address: str = "Praça Ferreira do Amaral, Macau",
    radius: int = 1100,
    rectangle: bool = False,
):
    aoi, utm_crs = geo.get_aoi(address=address, distance=radius, rectangle=rectangle)

    # TODO: Maybe iterative query and st plot?
    osm_tags = dataprep.osm_tags_from_settings(settings=LC_SETTINGS)
    # df = geo.query_osm(aoi=aoi, utm_crs=utm_crs)

    df_list = []
    for lc_class, osm_tags in LC_SETTINGS.items():
        df = geometries_from_polygon(polygon=aoi, tags=osm_tags)
        df = dataprep.cleanup_df(df=df, lc_class=lc_class, osm_tags=osm_tags)
        if lc_class == "streets":
            df = geo.adjust_street_width(df=df, utm_crs=utm_crs)
        df_list.append(df)

    df = pd.concat(df_list, axis=0)
    df = clip(df, aoi)
    ax = plotting.plot(df, drawing_kwargs=DRAW_SETTINGS)
    return ax


if __name__ == "__main__":
    ax = main()
    # plt.show()
