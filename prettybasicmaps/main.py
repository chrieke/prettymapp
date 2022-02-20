from geopandas import clip

from osmnx.geometries import geometries_from_polygon
from osmnx.utils import config

from prettybasicmaps.plotting import plot
from prettybasicmaps.geo import get_aoi, adjust_street_width
from prettybasicmaps.settings import LC_SETTINGS, DRAW_SETTINGS


from pyinstrument import Profiler


config(use_cache=True, log_console=False)


def get_geometries(
    address: str = "Praça Ferreira do Amaral, Macau",
    radius: int = 1100,
    rectangular: bool = False,
):
    # profiler = Profiler()
    # profiler.start()

    aoi, aoi_utm_crs = get_aoi(
        address=address, distance=radius, rectangular=rectangular
    )
    osm_tags = {k: v for d in LC_SETTINGS.values() for k, v in d.items()}
    df = geometries_from_polygon(polygon=aoi, tags=osm_tags)
    df = df.droplevel(level=0)
    df = df[df.geometry.geom_type != "Point"]
    # df = df.drop(df.columns.difference(["geometry"] + list(osm_tags.keys())), axis=1)
    df[df["highway"].notna()] = adjust_street_width(
        df=df[df["highway"].notna()], aoi_utm_crs=aoi_utm_crs
    )
    df = clip(df, aoi)

    df["landcover_class"] = None
    for lc_class, osm_tags in LC_SETTINGS.items():
        mask_lc_class = df[list(osm_tags.keys())].notna().sum(axis=1) != 0
        # # Remove mask elements that belong to other subtag
        # listed_osm_tags = {k: v for k, v in osm_tags.items() if isinstance(v, list)}
        # for tag, subtags in listed_osm_tags.items():
        #     mask_from_different_subtag = ~df[tag].isin(subtags) & df[tag].notna()
        #     mask_lc_class[mask_from_different_subtag] = False
        df["landcover_class"][mask_lc_class] = lc_class
    # Drop not assigned elements (part of multiple classes)
    df = df[~df["landcover_class"].isnull()]

    df = df.drop(df.columns.difference(["geometry", "landcover_class"]), axis=1)

    # profiler.stop()
    # #print(profiler.output_text(unicode=True, color=True))
    # profiler.open_in_browser()

    return df


if __name__ == "__main__":
    df = get_geometries()
    fig = plot(df, drawing_kwargs=DRAW_SETTINGS)
    # plt.show()
