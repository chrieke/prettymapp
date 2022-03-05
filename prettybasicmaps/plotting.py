from pathlib import Path
import colorsys

import numpy as np
from matplotlib.colors import ListedColormap, cnames, to_rgb
from matplotlib.pyplot import subplots
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse
from matplotlib.pyplot import Rectangle


def adjust_lightness(color, amount=0.5):
    # To avoid having the user background ec color value which is similar to background color
    try:
        c = cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def plot(
    df,
    drawing_kwargs,
    name_on=False,
    font_size=24,
    font_color="#2F3737",
    text_x=0,
    text_y=0,
    text_rotation=0,
    background_shape="rectangle",
    background_color="F2F4CB",
):
    """

    Args:
        df ():

    Returns:

    """
    fig, ax = subplots(1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200)
    ax.axis("off")

    xmin, ymin, xmax, ymax = df.total_bounds
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    xdif = xmax - xmin
    ydif = ymax - ymin

    if background_shape is not None:
        overhang = 0.02
        if background_shape == "rectangle":
            patch = Rectangle(
                (xmin - (xdif * overhang), ymin - (ydif * overhang)),
                xdif * (1 + 2 * overhang),
                ydif * (1 + 2 * overhang),
                color=background_color,
                ec=adjust_lightness(background_color, 0.78),  # todo: correct value?
                hatch="ooo...",
                zorder=-1,
                clip_on=True,
            )
            ax.add_patch(patch)
        elif background_shape == "circle":
            # axis aspect ratio no equal so ellipse required to display as circle
            maxd = max(xdif, ydif)
            width_ellipse = xdif / maxd * maxd * (1 + overhang)
            height_ellipse = ydif / maxd * maxd * (1 + overhang)
            ellipse = Ellipse(
                (xmid, ymid),
                width_ellipse,
                height_ellipse,
                facecolor=background_color,
                ec=adjust_lightness(background_color, 0.78),
                hatch="ooo...",
                zorder=-1,
                clip_on=True,
            )
            ax.add_artist(ellipse)
        ax.patch.set_zorder(
            -1
        )  # re-enables patch for background color that is deactivated with axis

    for lc_class in df["landcover_class"].unique():
        df_class = df[df["landcover_class"] == lc_class]
        draw_settings_class = drawing_kwargs[lc_class].copy()

        if "hatch_c" in draw_settings_class:
            # Matplotlib hatch color is set via ec. To have different edge color plot just the outlines again above.
            df_class.plot(
                ax=ax, fc="None", ec=draw_settings_class["hatch_c"], lw=1, zorder=6
            )
            draw_settings_class.pop("hatch_c")

        if lc_class == "urban":
            # Colormap formatting and random assignment
            draw_settings_class["cmap"] = ListedColormap(draw_settings_class["cmap"])
            df_class["randint"] = np.random.randint(0, 3, df_class.shape[0])
            df_class.plot(ax=ax, column="randint", **draw_settings_class)
        else:
            df_class.plot(ax=ax, **draw_settings_class)

    if name_on:
        x_text = xmid + text_x / 10 * xdif
        y_text = ymid + text_y / 10 * ydif

        _location_ = Path(__file__).resolve().parent
        ax.text(
            x=x_text,
            y=y_text,
            s="Stad van de Zon,\nHeerhugowaard, Netherlands",  # todo
            color=font_color,
            zorder=6,
            ha="center",
            rotation=text_rotation * -1,
            fontproperties=fm.FontProperties(
                fname=_location_ / "fonts/PermanentMarker-Regular.ttf"
            ),
            size=font_size,
        )

    return fig
