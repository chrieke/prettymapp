from geopandas import clip

from osmnx.geometries import geometries_from_polygon
from osmnx.utils import config

from prettymapp.geo import get_aoi, adjust_street_width, explode_mp
from prettymapp.settings import LC_SETTINGS, STYLES

config(use_cache=True, log_console=False)


def get_geometries(
    address: str = "Praça Ferreira do Amaral, Macau",
    radius: int = 1100,
    rectangular: bool = False,
):
    aoi, aoi_utm_crs = get_aoi(
        address=address, distance=radius, rectangular=rectangular
    )
    tags = {}
    for d in LC_SETTINGS.values():
        for k, v in d.items():
            try:
                tags.setdefault(k, []).extend(v)
            except TypeError:  # e.g. "building": True
                tags[k] = v

    df = geometries_from_polygon(polygon=aoi, tags=tags)
    df = df.droplevel(level=0)
    df = df[df.geometry.geom_type != "Point"]

    df[df["highway"].notna()] = adjust_street_width(
        df=df[df["highway"].notna()], aoi_utm_crs=aoi_utm_crs
    )
    df = clip(df, aoi)
    df = explode_mp(df)  # Simpler Polygonpatch plotting

    df["landcover_class"] = None
    for lc_class, osm_tags in LC_SETTINGS.items():
        tags_in_columns = set(osm_tags.keys()).intersection(list(df.columns))
        mask_lc_class = df[tags_in_columns].notna().sum(axis=1) != 0
        # Remove mask elements that belong to other subtag
        listed_osm_tags = {
            k: v
            for k, v in osm_tags.items()
            if isinstance(v, list) and k in tags_in_columns
        }
        for tag, subtags in listed_osm_tags.items():
            mask_from_different_subtag = ~df[tag].isin(subtags) & df[tag].notna()
            mask_lc_class[mask_from_different_subtag] = False
        df.loc[mask_lc_class, "landcover_class"] = lc_class
    # Drop not assigned elements (part of multiple classes)
    df = df[~df["landcover_class"].isnull()]

    df = df.drop(df.columns.difference(["geometry", "landcover_class"]), axis=1)

    return df
