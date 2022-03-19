import pickle
from pathlib import Path

from prettymapp.plotting import plot
from prettymapp.settings import DRAW_SETTINGS_1


def test_plot():
    _location_ = Path(__file__).resolve().parent
    with open(_location_ / "mock_data/df_pre_adjusting.pickle", "rb") as handle:
        df = pickle.load(handle)

    fig = plot(df, DRAW_SETTINGS_1)
    assert fig
