from typing import Any

from osmnx.geometries import geometries_from_polygon
from osmnx.utils import config
from geopandas import clip
from shapely.geometry import Polygon
import pandas as pd
from joblib import Parallel, delayed, cpu_count

from prettybasicmaps import geo
from prettybasicmaps import plotting
from prettybasicmaps.settings import LC_SETTINGS, DRAW_SETTINGS


config(use_cache=False)

def query_osm(aoi: Polygon, lc_class: str, osm_tags: dict, utm_crs: Any):
    df = geometries_from_polygon(polygon=aoi, tags=osm_tags)
    df["landcover_class"] = lc_class
    if lc_class == "streets":
        df = geo.adjust_street_width(df=df, utm_crs=utm_crs)  # requires columns
    df = df.drop(df.columns.difference(["landcover_class", "geometry"]), axis=1)
    # Drop not assigned elements (part of multiple classes)
    # df = df[~df["landcover_class"].isnull()]
    return df


def main(
    address: str = "Praça Ferreira do Amaral, Macau",
    radius: int = 1100,
    rectangular: bool = False,
):
    aoi, utm_crs = geo.get_aoi(address=address, distance=radius, rectangular=rectangular)

    parallel_pool = Parallel(n_jobs=cpu_count())
    delayed_funcs = [
        delayed(query_osm)(aoi, lc_class, osm_tags, utm_crs)
        for lc_class, osm_tags in LC_SETTINGS.items()
    ]
    df_list = parallel_pool(delayed_funcs)

    df = pd.concat(df_list, axis=0)
    df = df[df.geometry.geom_type != "Point"]
    df = clip(df, aoi)
    fig = plotting.plot(df, drawing_kwargs=DRAW_SETTINGS)
    return fig


if __name__ == "__main__":
    ax = main()
    # plt.show()
