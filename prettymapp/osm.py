from typing import Union
from pathlib import Path

from osmnx.features import features_from_polygon, features_from_xml
from osmnx import settings
from geopandas import clip, GeoDataFrame
from shapely.geometry import Polygon

from prettymapp.geo import explode_multigeometries
from prettymapp.settings import LANDCOVER_CLASSES

settings.use_cache = True
settings.log_console = False


def get_osm_tags(landcover_classes: dict = LANDCOVER_CLASSES):
    """
    Get relevant OSM tags for use with prettymapp
    
    Args:
        landcover_classes: Landcover selection settings, defaults to prettymapp.settings.LANDCOVER_CLASSES
        E.g.
        {
            "urban": {"building": True, "landuse": ["construction", "commercial"]},
            "water": {"natural": ["water", "bay"]},
        }
    """
    tags: dict = {}
    for sub_classes_dict in landcover_classes.values():
        for sub_class_name, subsub_classes in sub_classes_dict.items():
            if subsub_classes:  # Skip if False value
                if isinstance(subsub_classes, list):
                    tags.setdefault(sub_class_name, []).extend(subsub_classes)
                elif isinstance(subsub_classes, bool):
                    tags[sub_class_name] = subsub_classes
    return tags


def cleanup_osm_df(
    df: GeoDataFrame, aoi: Union[Polygon, None] = None, landcover_classes: dict = LANDCOVER_CLASSES
) -> GeoDataFrame:
    """
    Cleanup of queried osm geometries to relevant level for use with prettymapp
    
    Args:
        df: GeoDataFrame with queried OSM geometries
        aoi: Optional geographic boundary to filter elements
        landcover_classes: Landcover selection settings, defaults to prettymapp.settings.LANDCOVER_CLASSES
    """
    df = df.droplevel(level=0)
    df = df[~df.geometry.geom_type.isin(["Point", "MultiPoint"])]
    if aoi is not None:
        df = clip(df, aoi)
    df = explode_multigeometries(df)

    df["landcover_class"] = None
    for lc_class, osm_tags in landcover_classes.items():
        tags_in_columns = list(set(osm_tags.keys()).intersection(list(df.columns)))  # type: ignore
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


def get_osm_geometries(
    aoi: Polygon, landcover_classes: dict = LANDCOVER_CLASSES
) -> GeoDataFrame:
    """
    Query OSM features within a polygon geometry.

    Args:
        aoi: Polygon geometry query boundary.
        landcover_classes: Landcover selection settings, defaults to prettymapp.settings.LANDCOVER_CLASSES
    """
    tags = get_osm_tags(landcover_classes=landcover_classes)
    df = features_from_polygon(polygon=aoi, tags=tags)
    df = cleanup_osm_df(df, aoi, landcover_classes=landcover_classes)
    return df


def get_osm_geometries_from_xml(
    filepath: Union[str, Path], aoi: Union[Polygon, None] = None, landcover_classes: dict = LANDCOVER_CLASSES
) -> GeoDataFrame:
    """
    Query OSM features in an OSM-formatted XML file.

    Args:
        filepath: path to file containing OSM XML data
        aoi: Optional geographic boundary to filter elements
        landcover_classes: Landcover selection settings, defaults to prettymapp.settings.LANDCOVER_CLASSES
    """
    tags = get_osm_tags(landcover_classes=landcover_classes)
    df = features_from_xml(filepath, polygon=aoi, tags=tags)
    df = cleanup_osm_df(df, aoi, landcover_classes=landcover_classes)
    return df
