from pathlib import Path
import colorsys
from dataclasses import dataclass

import numpy as np
from geopandas import GeoDataFrame
from matplotlib.colors import ListedColormap, cnames, to_rgb
from matplotlib.pyplot import subplots, Rectangle
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse, Polygon
from matplotlib.collections import PatchCollection, LineCollection

from prettymapp.settings import STREETS_WIDTH


def adjust_lightness(color: str, amount=0.5) -> tuple:
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
    adjusted_c = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    return adjusted_c


def plot_poly_collection(ax, polys, cmap_values=None, colormap=None, **kwargs) -> None:
    """
    Plot a collection of shapely polygons.

    Faster then df.plot() as does not plot Polygons individually.

    Args:
        polys: Iterable of shapely polgons, not MultiPolgon.
        cmap_values: Assignment of colormap, should match length of geoms.
    """
    patches = [Polygon(np.asarray(poly.exterior)) for poly in polys]
    patchcollection = PatchCollection(patches, **kwargs)
    if cmap_values is not None:
        patchcollection.set_array(cmap_values)
        patchcollection.set_cmap(colormap)
    ax.add_collection(patchcollection, autolim=True)


def plot_linestring_collection(ax, lines, linewidth_values=None, **kwargs) -> None:
    """
    Plot a collection of shapely linestrings

    Faster then df.plot() as does not plot Polygons individually.

    Args:
        lines: Iterable of shapely linestrings, not MultiLinestring.
        linewidth_values: Assignment of colormap, should match length of geoms.
    """
    linecollection = LineCollection(lines, **kwargs)
    if linewidth_values is not None:
        linecollection.set_linewidth(linewidth_values)
    ax.add_collection(linecollection, autolim=True)


@dataclass
class Plot:
    df: GeoDataFrame
    aoi_bounds: list  # Not df bounds as could lead to weird plot shapes with unequal geometry distribution.
    draw_settings: dict
    shape: str = "circle"
    contour_width: int = 0
    contour_color: str = "#2F3537"
    name_on: bool = False
    name: str = "some name"
    font_size: int = 25
    font_color: str = "#2F3737"
    text_x: int = 0
    text_y: int = 0
    text_rotation: int = 0
    bg_shape: str = "rectangle"
    bg_buffer: int = 2
    bg_color: str = "#F2F4CB"

    def __post_init__(self):
        (
            self.xmin,
            self.ymin,
            self.xmax,
            self.ymax,
        ) = self.aoi_bounds
        # take from aoi geometry bounds, otherwise if no geometries on one side problematic.
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
        if self.contour_width:
            self.set_map_contour()
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

            if lc_class == "streets":
                df_class = df_class[df_class.geom_type == "LineString"]
                linewidth_values = list(
                    df_class["highway"].map(STREETS_WIDTH).fillna(1)
                )
                draw_settings_class["ec"] = draw_settings_class.pop("fc")
                plot_linestring_collection(
                    ax=self.ax,
                    lines=df_class.geometry,
                    linewidth_values=linewidth_values,
                    **draw_settings_class
                )
                continue
            else:
                df_class = df_class[df_class.geom_type == "Polygon"]

            if "hatch_c" in draw_settings_class:
                # Matplotlib hatch color is set via ec. hatch_c is used as the edge color here by plotting the outlines
                # again above.
                # Todo: why only with df.plot first round.
                df_class.plot(
                    ax=self.ax,
                    fc="None",
                    ec=draw_settings_class["hatch_c"],
                    lw=1,
                    zorder=6,
                )
                # plot_geom_collection(
                #     ax=self.ax,
                #     geoms=df_class.geometry,
                #     fc="None",
                #     ec=draw_settings_class["hatch_c"],
                #     lw=1,
                #     zorder=6,
                # )
                draw_settings_class.pop("hatch_c")

            if "cmap" in draw_settings_class:
                draw_settings_class["cmap"] = ListedColormap(
                    draw_settings_class["cmap"]
                )
                cmap_values = np.random.randint(0, 3, df_class.shape[0])
                # Patchcollection much faster than gpd.plot
                plot_poly_collection(
                    ax=self.ax,
                    polys=df_class.geometry,
                    cmap_values=cmap_values,
                    colormap=draw_settings_class["cmap"],
                    **draw_settings_class
                )
            else:
                plot_poly_collection(
                    ax=self.ax, polys=df_class.geometry, **draw_settings_class
                )

    def set_map_contour(self):
        if self.shape == "rectangle":
            patch = Rectangle(
                xy=(self.xmin, self.ymin),
                width=self.xdif,
                height=self.ydif,
                color="None",
                lw=self.contour_width,
                ec=self.contour_color,
                zorder=6,
                clip_on=True,
            )
            self.ax.add_patch(patch)
        elif self.shape == "circle":
            # axis aspect ratio no equal so ellipse required to display as circle
            ellipse = Ellipse(
                xy=(self.xmid, self.ymid),  # centroid
                width=self.xdif,
                height=self.ydif,
                color="None",
                lw=self.contour_width,
                ec=self.contour_color,
                zorder=6,
                clip_on=True,
            )
            self.ax.add_artist(ellipse)
            # re-enable patch for background color that is deactivated with axis
        self.ax.patch.set_zorder(6)

    def set_background(self):
        ec = adjust_lightness(self.bg_color, 0.78)
        if self.bg_shape == "rectangle":
            patch = Rectangle(
                xy=(self.xmin - self.bg_buffer_x, self.ymin - self.bg_buffer_y),
                width=self.xdif + 2 * self.bg_buffer_x,
                height=self.ydif + 2 * self.bg_buffer_y,
                color=self.bg_color,
                ec=ec,
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
        package_credit_text = "\n prettymaps | prettymapp"
        if add_package_credit:
            credit_text = credit_text + package_credit_text

        x = self.xmin + 0.8 * self.xdif
        y = self.ymin + 0.02 * self.ydif
        self.ax.text(x=x, y=y, s=credit_text, fontsize=9, zorder=6)
