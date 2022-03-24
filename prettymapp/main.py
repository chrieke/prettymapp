from osmnx.geometries import geometries_from_polygon
from osmnx.utils import config
from geopandas import clip, GeoDataFrame
from shapely.geometry import Polygon

from prettymapp.geo import explode_multigeometries
from prettymapp.settings import LC_SETTINGS

config(use_cache=True, log_console=False)


def get_osm_geometries(aoi: Polygon) -> GeoDataFrame:
    tags: dict = {}
    for d in LC_SETTINGS.values():  # type: ignore
        for k, v in d.items():  # type: ignore
            try:
                tags.setdefault(k, []).extend(v)
            except TypeError:  # e.g. "building": True
                tags[k] = v

    df = geometries_from_polygon(polygon=aoi, tags=tags)
    df = df.droplevel(level=0)
    df = df[~df.geometry.geom_type.isin(["Point", "MultiPoint"])]

    df = clip(df, aoi)
    df = explode_multigeometries(df)

    df["landcover_class"] = None
    for lc_class, osm_tags in LC_SETTINGS.items():
        tags_in_columns = set(osm_tags.keys()).intersection(list(df.columns))  # type: ignore
        mask_lc_class = df[tags_in_columns].notna().sum(axis=1) != 0
        # Remove mask elements that belong to other subtag
        listed_osm_tags = {
            k: v
            for k, v in osm_tags.items()  # type: ignore
            if isinstance(v, list) and k in tags_in_columns
        }
        for tag, subtags in listed_osm_tags.items():
            mask_from_different_subtag = ~df[tag].isin(subtags) & df[tag].notna()
            mask_lc_class[mask_from_different_subtag] = False
        df.loc[mask_lc_class, "landcover_class"] = lc_class
    # Drop not assigned elements (part of multiple classes)
    df = df[~df["landcover_class"].isnull()]
    df = df.drop(
        df.columns.difference(["geometry", "landcover_class", "highway"]), axis=1
    )

    return df
