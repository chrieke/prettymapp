import matplotlib.pyplot as plt
from descartes import PolygonPatch


def plot(df, aoi):
    """

    Args:
            df ():

    Returns:

    """
    _, ax = plt.subplots(1, 1, figsize=(12, 12))
    # ax.axis("off")
    # ax.axis("equal")
    street_kwargs = {"fc": "#2F3737", "ec": "#475657"}
    geom = df.plot(ax=ax, **street_kwargs)
    ax.set_facecolor("#F2F4CB")  # background
    ax.add_patch(PolygonPatch(aoi, **street_kwargs))  # outline
    ax.add_patch(PolygonPatch(geom, **street_kwargs))

    plt.show()
