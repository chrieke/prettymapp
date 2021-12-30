from geopandas import GeoDataFrame


def osm_tags_from_settings(settings: dict) -> dict:
    osm_tags = {}
    for element in settings.values():
        for k, v in element.items():
            try:
                osm_tags.setdefault(k, []).extend(v)
            except TypeError:
                osm_tags[k] = v

    return osm_tags


def cleanup_df(df: GeoDataFrame, lc_settings: dict) -> GeoDataFrame:
    # Drop point geometries
    df = df[df.geometry.geom_type != "Point"]

    # Summarize to lc_classes
    df["landcover_class"] = None
    for lc_class, osm_tags in lc_settings.items():
        mask_lc_class = df[list(osm_tags.keys())].notna().sum(axis=1) != 0

        # Remove mask elements that belong to other subtag
        # TODO: Easier if positive selection always?
        listed_osm_tags = {k: v for k, v in osm_tags.items() if isinstance(v, list)}
        for tag, subtags in listed_osm_tags.items():
            mask_from_different_subtag = ~df[tag].isin(subtags) & df[tag].notna()
            mask_lc_class[mask_from_different_subtag] = False

        df["landcover_class"][mask_lc_class] = lc_class

    df = df.drop(
        df.columns.difference(["landcover_class", "geometry", "highway"]), axis=1
    )

    # Drop not assigned elements (part of multiple classes)
    # TODO: Better solution?
    df = df[~df["landcover_class"].isnull()]

    return df
