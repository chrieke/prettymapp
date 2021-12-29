import numpy as np


def cleanup_df(df, tags):
    # Drop point geometries
    df = df[df.geometry.geom_type != "Point"]

    # Drop irrelevant columns
    relevant_cols = list(tags.keys())
    df["osm_type"] = df[relevant_cols].columns[np.where(df[relevant_cols].notna())[1]]
    df = df.drop(
        df.columns.difference(["osm_type", "geometry"] + relevant_cols), axis=1
    )
    return df
