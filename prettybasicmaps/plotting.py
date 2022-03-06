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


@dataclass
class Plot:
    df: GeoDataFrame
    drawing_kwargs: dict
    name_on: bool = False
    name: str = ""
    font_size: int = 24
    font_color: str = "#2F3737"
    text_x: int = 0
    text_y: int = 0
    text_rotation: int = 0
    bg_shape: str = "rectangle"
    bg_color: str = "F2F4CB"

    def __post_init__(self):
        self.xmin, self.ymin, self.xmax, self.ymax = self.df.total_bounds
        self.xmid = (self.xmin + self.xmax) / 2
        self.ymid = (self.ymin + self.ymax) / 2
        self.xdif = self.xmax - self.xmin
        self.ydif = self.ymax - self.ymin

        self.fig, self.ax = subplots(
            1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200
        )
        self.ax.axis("off")
        self.ax.set_xlim(self.xmin, self.xmax)
        self.ax.set_ylim(self.ymin, self.ymax)

    def plot_all(self):
        self.plot_geometries()
        if self.bg_shape is not None:
            self.set_background()
        if self.name_on:
            self.set_name()
        self.set_credits(add_package_credit=True)
        return self.fig

    def plot_geometries(self):
        for lc_class in self.df["landcover_class"].unique():
            df_class = self.df[self.df["landcover_class"] == lc_class]
            draw_settings_class = self.drawing_kwargs[lc_class].copy()

            if "hatch_c" in draw_settings_class:
                # Matplotlib hatch color is set via ec. To have different edge color plot just the outlines again above.
                df_class.plot(
                    ax=self.ax,
                    fc="None",
                    ec=draw_settings_class["hatch_c"],
                    lw=1,
                    zorder=6,
                )
                draw_settings_class.pop("hatch_c")

            if lc_class == "urban":
                # Colormap formatting and random assignment
                draw_settings_class["cmap"] = ListedColormap(
                    draw_settings_class["cmap"]
                )
                df_class["randint"] = np.random.randint(0, 3, df_class.shape[0])
                df_class.plot(ax=self.ax, column="randint", **draw_settings_class)
            else:
                df_class.plot(ax=self.ax, **draw_settings_class)

    def set_background(self):
        overhang = 0.02
        if self.bg_shape == "rectangle":
            patch = Rectangle(
                (
                    self.xmin - (self.xdif * overhang),
                    self.ymin - (self.ydif * overhang),
                ),
                self.xdif * (1 + 2 * overhang),
                self.ydif * (1 + 2 * overhang),
                color=self.bg_color,
                ec=adjust_lightness(self.bg_color, 0.78),  # todo: correct value?
                hatch="ooo...",
                zorder=-1,
                clip_on=True,
            )
            self.ax.add_patch(patch)
        elif self.bg_shape == "circle":
            # axis aspect ratio no equal so ellipse required to display as circle
            maxd = max(self.xdif, self.ydif)
            width_ellipse = self.xdif / maxd * maxd * (1 + overhang)
            height_ellipse = self.ydif / maxd * maxd * (1 + overhang)
            ellipse = Ellipse(
                (self.xmid, self.ymid),
                width_ellipse,
                height_ellipse,
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
        x_text = self.xmid + text_x / 10 * self.xdif
        y_text = self.ymid + text_y / 10 * self.ydif

        _location_ = Path(__file__).resolve().parent
        fontproperties = fm.FontProperties(
            fname=_location_ / "fonts/PermanentMarker-Regular.ttf"
        )
        self.ax.text(
            x=x_text,
            y=y_text,
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
