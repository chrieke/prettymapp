import pickle
from pathlib import Path

from prettybasicmaps import plotting
from prettybasicmaps.settings import DRAW_SETTINGS


def test_plot():
    _location_ = Path(__file__).resolve().parent
    with open(_location_ / "mock_data/df_pre_dissolve.pickle", "rb") as handle:
        df = pickle.load(handle)

    ax = plotting.plot(df, DRAW_SETTINGS)
    assert ax
