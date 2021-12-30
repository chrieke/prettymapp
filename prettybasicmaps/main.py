from osmnx.geometries import geometries_from_polygon
from osmnx.utils import config
from geopandas import clip

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
    df = geometries_from_polygon(polygon=aoi, tags=osm_tags)

    df = clip(df, aoi)
    df = dataprep.cleanup_df(df=df, lc_settings=LC_SETTINGS)
    df_utm = geo.adjust_street_width(df=df, utm_crs=utm_crs)

    ax = plotting.plot(df_utm, drawing_kwargs=DRAW_SETTINGS)
    return ax


if __name__ == "__main__":
    ax = main()
    # plt.show()
