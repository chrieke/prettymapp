from pathlib import Path
import colorsys

import numpy as np
from matplotlib.colors import ListedColormap, cnames, to_rgb
from matplotlib.pyplot import subplots
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse
from matplotlib.pyplot import Rectangle


def adjust_lightness(color: str, amount=0.5):
    """
    Helper to avoid having the user background ec color value which is similar to background color.

    via https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    """
    #
    try:
        c = cnames[color]
    except KeyError:
        c = color
    c = colorsys.rgb_to_hls(*to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])


def set_name(
    ax,
    bounds,
    name: str,
    font_size: int,
    font_color: str,
    text_x: int,
    text_y: int,
    text_rotation: int,
):
    xmin, ymin, xmax, ymax = bounds
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    xdif = xmax - xmin
    ydif = ymax - ymin

    x_text = xmid + text_x / 10 * xdif
    y_text = ymid + text_y / 10 * ydif

    _location_ = Path(__file__).resolve().parent
    ax.text(
        x=x_text,
        y=y_text,
        s=name,
        color=font_color,
        zorder=6,
        ha="center",
        rotation=text_rotation * -1,
        fontproperties=fm.FontProperties(
            fname=_location_ / "fonts/PermanentMarker-Regular.ttf"
        ),
        size=font_size,
    )


def set_background(ax, bounds, bg_shape: str, bg_color: str):
    xmin, ymin, xmax, ymax = bounds
    xmid = (xmin + xmax) / 2
    ymid = (ymin + ymax) / 2
    xdif = xmax - xmin
    ydif = ymax - ymin

    overhang = 0.02
    if bg_shape == "rectangle":
        patch = Rectangle(
            (xmin - (xdif * overhang), ymin - (ydif * overhang)),
            xdif * (1 + 2 * overhang),
            ydif * (1 + 2 * overhang),
            color=bg_color,
            ec=adjust_lightness(bg_color, 0.78),  # todo: correct value?
            hatch="ooo...",
            zorder=-1,
            clip_on=True,
        )
        ax.add_patch(patch)
    elif bg_shape == "circle":
        # axis aspect ratio no equal so ellipse required to display as circle
        maxd = max(xdif, ydif)
        width_ellipse = xdif / maxd * maxd * (1 + overhang)
        height_ellipse = ydif / maxd * maxd * (1 + overhang)
        ellipse = Ellipse(
            (xmid, ymid),
            width_ellipse,
            height_ellipse,
            facecolor=bg_color,
            ec=adjust_lightness(bg_color, 0.78),
            hatch="ooo...",
            zorder=-1,
            clip_on=True,
        )
        ax.add_artist(ellipse)
    ax.patch.set_zorder(
        -1
    )  # re-enables patch for background color that is deactivated with axis


def plot(
    df,
    drawing_kwargs,
    name_on: bool = False,
    font_size: int = 24,
    font_color: str = "#2F3737",
    text_x: int = 0,
    text_y: int = 0,
    text_rotation: int = 0,
    bg_shape: str = "rectangle",
    bg_color: str = "F2F4CB",
):
    """

    Args:
        df ():

    Returns:

    """
    fig, ax = subplots(1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200)
    ax.axis("off")

    bounds = df.total_bounds

    if bg_shape is not None:
        set_background(
            ax=ax,
            bounds=bounds,
            bg_shape=bg_shape,
            bg_color=bg_color,
        )

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
        set_name(ax, bounds, name, font_size, font_color, text_x, text_y, text_rotation)

    return fig
