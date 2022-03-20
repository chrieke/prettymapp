# import pickle
from pathlib import Path

from matplotlib.pyplot import subplots
from shapely.geometry import Polygon
from matplotlib.collections import PatchCollection

from prettymapp.plotting import Plot, adjust_lightness, plot_geom_collection
from prettymapp.settings import STYLES

#
#
# def test_plot():
#     _location_ = Path(__file__).resolve().parent
#     with open(_location_ / "mock_data/df_pre_adjusting.pickle", "rb") as handle:
#         df = pickle.load(handle)
#
#     fig = plot(df, DRAW_SETTINGS_1)
#     assert fig


def test_adjust_lightness():
    color = adjust_lightness("#FFC857")
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert color == (0.6705882352941177, 0.4510504201680673, 0.0)


def test_plot_geom_collection():
    fig, ax = subplots(1, 1, figsize=(12, 12), constrained_layout=True, dpi=1200)
    poly = Polygon([[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]])
    geoms = [poly] * 3
    patches = plot_geom_collection(ax, geoms)
    assert isinstance(patches, PatchCollection)
