import base64
from io import StringIO, BytesIO
import unicodedata
import re
from typing import Any
import io
import json

from matplotlib.pyplot import figure
import streamlit as st
from geopandas import GeoDataFrame
from shapely.geometry import Polygon

from prettymapp.plotting import Plot
from prettymapp.osm import get_osm_geometries
from prettymapp.settings import STYLES


@st.cache_data(show_spinner=False, hash_funcs={Polygon: lambda x: json.dumps(x.__geo_interface__)})
def st_get_osm_geometries(aoi):
    """Wrapper to enable streamlit caching for package function"""
    df = get_osm_geometries(aoi=aoi)
    return df


@st.cache_data(show_spinner=False)
def st_plot_all(_df: GeoDataFrame, **kwargs):
    """Wrapper to enable streamlit caching for package function"""
    fig = Plot(_df, **kwargs).plot_all()
    return fig


def get_colors_from_style(style: str) -> dict:
    """
    Returns dict of landcover_class : color
    """
    lc_class_colors = {}
    for lc_class, class_style in STYLES[style].items():
        colors = class_style.get("cmap", class_style.get("fc"))
        if isinstance(colors, list):
            for idx, color in enumerate(colors):
                lc_class_colors[f"{lc_class}_{idx}"] = color
        else:
            lc_class_colors[lc_class] = colors
    return lc_class_colors


def plt_to_svg(fig: figure) -> str:
    imgdata = StringIO()
    fig.savefig(
        imgdata, format="svg", pad_inches=0, bbox_inches="tight", transparent=True
    )
    imgdata.seek(0)
    svg_string = imgdata.getvalue()
    return svg_string


def svg_to_html(svg_string: str) -> str:
    b64 = base64.b64encode(svg_string.encode("utf-8")).decode("utf-8")
    css_justify = "center"
    css = '<p style="text-align:center; display: flex; flex-direction: column; justify-content: {};">'.format(
        css_justify
    )
    html = r'{}<img src="data:image/svg+xml;base64,{}"/>'.format(css, b64)
    return html


def plt_to_href(fig: figure, filename: str):
    buf = BytesIO()
    fig.savefig(buf, format="png", pad_inches=0, bbox_inches="tight", transparent=True)
    img_str = base64.b64encode(buf.getvalue()).decode()
    href = f'<a href="data:file/txt;base64,{img_str}" download="{filename}"></a>'
    return href


def slugify(value: Any, allow_unicode: bool = False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")


def gdf_to_bytesio_geojson(geodataframe):
    geojson_object = io.BytesIO()
    geodataframe.to_file(geojson_object, driver="GeoJSON")
    return geojson_object
