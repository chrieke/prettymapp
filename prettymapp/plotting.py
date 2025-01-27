from pathlib import Path
import colorsys
from typing import Tuple, List
from dataclasses import dataclass

from dataclasses import field
from geopandas.plotting import _plot_polygon_collection, _plot_linestring_collection
from geopandas import GeoDataFrame
import numpy as np
from matplotlib.colors import ListedColormap, cnames, to_rgb
from matplotlib.pyplot import subplots, Rectangle
import matplotlib.font_manager as fm
from matplotlib.patches import Ellipse
import matplotlib.patheffects as PathEffects

from prettymapp.settings import STREETS_WIDTH, STYLES


@dataclass
class Plot:
    """
    Main plotting class for prettymapp.
    
    Args:
        df: GeoDataFrame with the geometries to plot
        aoi_bounds: List of minx, miny, maxx, maxy coordinates, specifying the map extent
        draw_settings: Dictionary of color & draw settings, see prettymapp.settings.STYLES
        
        # Map layout
        shape: the map shape, "circle" or "rectangle"
        contour_width: width of the map contour, defaults to 0
        contour_color: color of the map contour, defaults to "#2F3537"
        
        # Optional map text settings e.g. to display location name
        name_on: whether to display the location name, defaults to False
        name: the location name to display, defaults to "some name"
        font_size: font size of the location name, defaults to 25
        font_color: color of the location name, defaults to "#2F3737"
        text_x: x-coordinate of the location name, defaults to 0
        text_y: y-coordinate of the location name, defaults to 0
        text_rotation: rotation of the location name, defaults to 0
        credits: Boolean whether to display the OSM&package credits, defaults to True
        
        # Map background settings
        bg_shape: the map background shape, "circle" or "rectangle", defaults to "circle"
        bg_buffer: buffer around the map, defaults to 2
        bg_color: color of the map background, defaults to "#F2F4CB"
    """
    df: GeoDataFrame
    aoi_bounds: List[
        float
    ]  # Not df bounds as could lead to weird plot shapes with unequal geometry distribution.
    draw_settings: dict = field(default_factory=lambda: STYLES["Peach"])
    # Map layout settings
    shape: str = "circle"
    contour_width: int = 0
    contour_color: str = "#2F3537"
    # Optional map text settings e.g. to display location name
    name_on: bool = False
    name: str = "some name"
    font_size: int = 25
    font_color: str = "#2F3737"
    text_x: int = 0
    text_y: int = 0
    text_rotation: int = 0
    credits: bool = True
    # Map background settings
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
        # take from aoi geometry bounds, otherwise probelematic if unequal geometry distribution over plot.
        self.xmid = (self.xmin + self.xmax) / 2
        self.ymid = (self.ymin + self.ymax) / 2
        self.xdif = self.xmax - self.xmin
        self.ydif = self.ymax - self.ymin

        self.bg_buffer_x = (self.bg_buffer / 100) * self.xdif
        self.bg_buffer_y = (self.bg_buffer / 100) * self.ydif

        self.fig, self.ax = subplots(
            1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200
        )
        self.ax.set_aspect(1 / np.cos(self.ymid * np.pi / 180))

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
        if self.credits:
            self.set_credits()

        return self.fig

    def set_geometries(self):
        """
        Avoids using geodataframe.plot() as this uses plt.draw(), but for the app, the figure needs to be rendered
        only in st.pyplot. Shaves off 1 sec.
        """
        for lc_class in self.df["landcover_class"].unique():
            df_class = self.df[self.df["landcover_class"] == lc_class]
            try:
                draw_settings_class = self.draw_settings[lc_class].copy()
            except KeyError:
                continue

            # pylint: disable=no-else-continue
            if lc_class == "streets":
                df_class = df_class[df_class.geom_type == "LineString"]
                linewidth_values = list(
                    df_class["highway"].map(STREETS_WIDTH).fillna(1)
                )
                draw_settings_class["ec"] = draw_settings_class.pop("fc")
                linecollection = _plot_linestring_collection(
                    ax=self.ax, geoms=df_class.geometry, **draw_settings_class
                )
                linecollection.set_linewidth(linewidth_values)
                self.ax.add_collection(linecollection, autolim=True)
                continue
            else:
                df_class = df_class[df_class.geom_type == "Polygon"]

            if "hatch_c" in draw_settings_class:
                # Matplotlib hatch color is set via ec. hatch_c is used as the edge color here by plotting the outlines
                # again above.
                _plot_polygon_collection(
                    ax=self.ax,
                    geoms=df_class.geometry,
                    fc="None",
                    ec=draw_settings_class["hatch_c"],
                    lw=1,
                    zorder=6,
                )
                draw_settings_class.pop("hatch_c")

            if "cmap" in draw_settings_class:
                cmap = ListedColormap(draw_settings_class["cmap"])
                draw_settings_class.pop("cmap")
                cmap_values = np.random.randint(0, 3, df_class.shape[0])
                _plot_polygon_collection(
                    ax=self.ax,
                    geoms=df_class.geometry,
                    values=cmap_values,
                    cmap=cmap,
                    **draw_settings_class
                )
            else:
                _plot_polygon_collection(
                    ax=self.ax, geoms=df_class.geometry, **draw_settings_class
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
        fpath = _location_ / "fonts/PermanentMarker-Regular.ttf"
        fontproperties = fm.FontProperties(fname=fpath.resolve())
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

    def set_credits(self, text: str = "© OpenStreetMap\n prettymapp | prettymaps", 
                x: float | None = None, 
                y: float | None = None, 
                fontsize: int = 9, 
                zorder: int = 6):
        """
        Add OSM credits. Defaults to lower right corner of map.
        """
        if x is None:
            x = self.xmin + 0.87 * self.xdif
        if y is None:
            y = self.ymin - 0.70 * self.bg_buffer_y
        text = self.ax.text(x=x, y=y, s=text, c="w", fontsize=fontsize, zorder=zorder)
        text.set_path_effects([PathEffects.withStroke(linewidth=3, foreground="black")])


def adjust_lightness(color: str, amount: float = 0.5) -> Tuple[float, float, float]:
    """
    In-/Decrease color brightness amount by factor.

    Helper to avoid having the user define background ec color value which is similar to background color.

    via https://stackoverflow.com/questions/37765197/darken-or-lighten-a-color-in-matplotlib
    """
    try:
        c = cnames[color]
    except KeyError:
        c = color
    c = colorsys.rgb_to_hls(*to_rgb(c))
    adjusted_c = colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])
    return adjusted_c
