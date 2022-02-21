from pathlib import Path

import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.pyplot import subplots
import matplotlib.font_manager as fm


def plot(df, drawing_kwargs, name_on=False, font_size=24, font_color="#2F3737"):
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

    if name_on:
        xmin, ymin, xmax, ymax = df.total_bounds
        xmid = (xmin + xmax) / 2
        dify = ymax - ymin
        _location_ = Path(__file__).resolve().parent
        ax.text(
            x=xmid,
            y=ymin + 0.305 * dify,
            s="Stad van de Zon,\nHeerhugowaard, Netherlands",
            color=font_color,
            zorder=6,
            ha="center",
            # rotation = +1.75,
            fontproperties=fm.FontProperties(
                fname=_location_ / "fonts/PermanentMarker-Regular.ttf"
            ),
            size=font_size,
        )

    return fig
