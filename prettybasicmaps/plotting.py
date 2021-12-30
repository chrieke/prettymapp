from matplotlib.pyplot import subplots

import numpy as np
from matplotlib.colors import ListedColormap


def plot(df, drawing_kwargs):
    """

    Args:
        df ():

    Returns:

    """
    _, ax = subplots(1, 1, figsize=(12, 12))
    ax.axis("off")
    ax.axis("equal")
    # ax.set_facecolor("#F2F4CB")  # background

    for lc_class in df["landcover_class"].unique():
        if lc_class == "urban":
            drawing_kwargs[lc_class]["cmap"] = ListedColormap(
                drawing_kwargs[lc_class]["cmap"]
            )
            df_urban = df[df["landcover_class"] == lc_class]
            df_urban["randint"] = np.random.randint(0, 3, df_urban.shape[0])
            df_urban.plot(ax=ax, column="randint", **drawing_kwargs[lc_class])
        else:
            df[df["landcover_class"] == lc_class].plot(
                ax=ax, **drawing_kwargs[lc_class]
            )

    return ax
