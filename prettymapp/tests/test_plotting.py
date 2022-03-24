from matplotlib.pyplot import subplots
from shapely.geometry import Polygon, LineString

from prettymapp.plotting import (
    adjust_lightness,
    plot_poly_collection,
    plot_linestring_collection,
)


def test_adjust_lightness():
    color = adjust_lightness("#FFC857")
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert color == (0.6705882352941177, 0.4510504201680673, 0.0)


def test_plot_poly_collection():
    _, ax = subplots(1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200)
    poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    geoms = [poly] * 3
    plot_poly_collection(ax, geoms)


def test_plot_linestring_collection():
    _, ax = subplots(1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200)
    linestring = LineString([(0, 0), (1, 1)])
    geoms = [linestring] * 3
    plot_linestring_collection(ax, geoms)

    #
