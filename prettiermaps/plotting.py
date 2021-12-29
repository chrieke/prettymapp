import matplotlib.pyplot as plt
from descartes import PolygonPatch


def plot(df):
    """

    Args:
            df ():

    Returns:

    """
    fig, ax = plt.subplots(1, 1, figsize=(12, 12))
    # ax.axis("off")
    # ax.axis("equal")
    drawing_kwargs = {"fc": "#2F3737", "ec": "#475657"}
    geom = df.dissolve().plot(
        ax=ax, **drawing_kwargs
    )  # multilinestring #TODO probably multiple mls from gdf
    plt.show()
    ax.add_patch(PolygonPatch(geom, **drawing_kwargs))
    plt.show()
