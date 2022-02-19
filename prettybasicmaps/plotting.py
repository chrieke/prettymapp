import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import subplots


def plot(df, drawing_kwargs):
    """

    Args:
        df ():

    Returns:

    """
    fig, ax = subplots(1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200)
    ax.axis("off")
    ax.axis("equal")
    # ax.set_facecolor("#F2F4CB")  # background

    for lc_class in df["landcover_class"].unique():
        if lc_class == "urban":
            urban_drawing_kwargs = drawing_kwargs[lc_class].copy()
            urban_drawing_kwargs["cmap"] = ListedColormap(urban_drawing_kwargs["cmap"])
            df_urban = df[df["landcover_class"] == lc_class]
            df_urban["randint"] = np.random.randint(0, 3, df_urban.shape[0])
            df_urban.plot(ax=ax, column="randint", **urban_drawing_kwargs)
        else:
            df[df["landcover_class"] == lc_class].plot(
                ax=ax, **drawing_kwargs[lc_class]
            )

    return fig
