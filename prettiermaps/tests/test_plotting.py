import pickle
from pathlib import Path

import pytest
import matplotlib.pyplot as plt

from prettiermaps import plotting
from prettiermaps.main import DRAWING_KWARGS


def test_plot():
    _location_ = Path(__file__).resolve().parent
    with open(_location_ / "mock_data/df_pre_dissolve.pickle", "rb") as handle:
        df = pickle.load(handle)

    ax = plotting.plot(df, DRAWING_KWARGS)
    assert ax
    # plt.show()
