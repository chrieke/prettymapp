import matplotlib.pyplot as plt

# from descartes import PolygonPatch
import numpy as np
from matplotlib.colors import ListedColormap


def plot(df, drawing_kwargs):
    """

    Args:
            df ():

    Returns:

    """
    _, ax = plt.subplots(1, 1, figsize=(12, 12))
    # ax.axis("off")
    # ax.axis("equal")
    ax.set_facecolor("#F2F4CB")  # background

    for object_type in df.osm_type.unique():
        if object_type == "building":
            df_buildings = df[df.osm_type == object_type]
            df_buildings["rand"] = np.random.randint(0, 3, df_buildings.shape[0])
            drawing_kwargs[object_type]["cmap"] = ListedColormap(
                drawing_kwargs[object_type]["cmap"]
            )
            df_buildings.plot(ax=ax, column="rand", **drawing_kwargs[object_type])
        else:
            df[df.osm_type == object_type].plot(ax=ax, **drawing_kwargs[object_type])
    # ax.add_patch(PolygonPatch(geom, **kwargs_streets))

    return ax
