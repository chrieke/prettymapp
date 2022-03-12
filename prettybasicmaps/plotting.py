from pathlib import Path
import colorsys
from dataclasses import dataclass

import numpy as np
from geopandas import GeoDataFrame
from matplotlib.colors import ListedColormap, cnames, to_rgb
from matplotlib.pyplot import subplots
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse
from matplotlib.pyplot import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib.patches import Polygon


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


def plot_polygon_collection(
    ax,
    geoms,
    values=None,
    colormap="Set1",
    facecolor=None,
    edgecolor=None,
    alpha=0.5,
    linewidth=1.0,
    **kwargs
):
    """
    Plot a collection of Polygon geometries

    Faster then df.plot() as does not plot individual Polygons.

    Args:
        geoms: Iteratble of shapely objects, not MultiPolgon.
    """
    patches = []
    for poly in geoms:
        # if poly.has_z:
        #     poly = shapely.geometry.Polygon(zip(*poly.exterior.xy))
        patches.append(Polygon(np.asarray(poly.exterior)))
    patches = PatchCollection(
        patches,
        facecolor=facecolor,
        linewidth=linewidth,
        edgecolor=edgecolor,
        alpha=alpha,
        **kwargs
    )

    if values is not None:
        patches.set_array(values)
        patches.set_cmap(colormap)

    ax.add_collection(patches, autolim=True)
    ax.autoscale_view()
    return patches


@dataclass
class Plot:
    df: GeoDataFrame
    draw_settings: dict
    name_on: bool = False
    name: str = ""
    font_size: int = 24
    font_color: str = "#2F3737"
    text_x: int = 0
    text_y: int = 0
    text_rotation: int = 0
    bg_shape: str = "rectangle"
    bg_buffer: int = 2
    bg_color: str = "F2F4CB"

    def __post_init__(self):
        self.xmin, self.ymin, self.xmax, self.ymax = self.df.total_bounds
        self.xmid = (self.xmin + self.xmax) / 2
        self.ymid = (self.ymin + self.ymax) / 2
        self.xdif = self.xmax - self.xmin
        self.ydif = self.ymax - self.ymin

        self.bg_buffer_x = (self.bg_buffer / 100) * self.xdif
        self.bg_buffer_y = (self.bg_buffer / 100) * self.ydif

        self.fig, self.ax = subplots(
            1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200
        )
        self.ax.set_aspect("equal")
        self.ax.axis("off")
        self.ax.set_xlim(self.xmin - self.bg_buffer_x, self.xmax + self.bg_buffer_x)
        self.ax.set_ylim(self.ymin - self.bg_buffer_y, self.ymax + self.bg_buffer_y)

    def plot_all(self):
        if self.bg_shape is not None:
            self.set_background()
        self.set_geometries()
        if self.name_on:
            self.set_name()
        self.set_credits(add_package_credit=True)

        return self.fig

    def set_geometries(self):
        for lc_class in self.df["landcover_class"].unique():
            df_class = self.df[self.df["landcover_class"] == lc_class]
            try:
                draw_settings_class = self.draw_settings[lc_class].copy()
            except KeyError:
                continue

            if "hatch_c" in draw_settings_class:
                # Matplotlib hatch color is set via ec. hatch_c is used as the edge color here by plotting the outlines
                # again above.
                df_class.plot(
                    ax=self.ax,
                    fc="None",
                    ec=draw_settings_class["hatch_c"],
                    lw=1,
                    zorder=6,
                )
                draw_settings_class.pop("hatch_c")

            if "cmap" in draw_settings_class:
                # Colormap formatting and random assignment
                draw_settings_class["cmap"] = ListedColormap(
                    draw_settings_class["cmap"]
                )
                # Slower
                # df_class["randint"] = np.random.randint(0, 3, df_class.shape[0])
                # df_class.plot(ax=self.ax, column="randint", **draw_settings_class)
                # plot_polygon_collection(
                #     ax=self.ax,
                #     column="randint",
                #     geoms=df_class.geometry,
                #     **draw_settings_class
                # )
                values = np.random.randint(0, 3, df_class.shape[0])
                plot_polygon_collection(
                    ax=self.ax,
                    values=values,
                    colormap=draw_settings_class["cmap"],
                    geoms=df_class.geometry,
                    **draw_settings_class
                )
            else:
                # TODO: fix colors
                plot_polygon_collection(
                    ax=self.ax, geoms=df_class.geometry, **draw_settings_class
                )
                # df_class.plot(ax=self.ax, **draw_settings_class) # much slower

    def set_background(self):
        if self.bg_shape == "rectangle":
            patch = Rectangle(
                xy=(self.xmin - self.bg_buffer_x, self.ymin - self.bg_buffer_y),
                width=self.xdif + 2 * self.bg_buffer_x,
                height=self.ydif + 2 * self.bg_buffer_y,
                color=self.bg_color,
                ec=adjust_lightness(self.bg_color, 0.78),  # todo: correct value?
                hatch="ooo...",
                zorder=-1,
                clip_on=True,
            )
            self.ax.add_patch(patch)
        elif self.bg_shape == "circle":
            # axis aspect ratio no equal so ellipse required to display as circle
            ellipse = Ellipse(
                xy=(self.xmid, self.ymid),  # centroid
                width=self.xdif + 2 * self.bg_buffer_x,
                height=self.ydif + 2 * self.bg_buffer_y,
                facecolor=self.bg_color,
                ec=adjust_lightness(self.bg_color, 0.78),
                hatch="ooo...",
                zorder=-1,
                clip_on=True,
            )
            self.ax.add_artist(ellipse)
        # re-enable patch for background color that is deactivated with axis
        self.ax.patch.set_zorder(-1)

    def set_name(self):
        x = self.xmid + self.text_x / 100 * self.xdif
        y = self.ymid + self.text_y / 100 * self.ydif

        _location_ = Path(__file__).resolve().parent
        fontproperties = fm.FontProperties(
            fname=_location_ / "fonts/PermanentMarker-Regular.ttf"
        )
        self.ax.text(
            x=x,
            y=y,
            s=self.name,
            color=self.font_color,
            zorder=6,
            ha="center",
            rotation=self.text_rotation * -1,
            fontproperties=fontproperties,
            size=self.font_size,
        )

    def set_credits(self, add_package_credit=False):
        credit_text = "© OpenStreetMap"
        package_credit_text = "\n prettymaps | pretty(basic)maps"
        if add_package_credit:
            credit_text = credit_text + package_credit_text

        x = self.xmin + 0.8 * self.xdif
        y = self.ymin + 0.02 * self.ydif
        self.ax.text(x=x, y=y, s=credit_text, fontsize=9, zorder=6)
