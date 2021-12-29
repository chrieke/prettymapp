import pickle
from pathlib import Path

import pytest

from prettiermaps import plotting


@pytest.mark.skip
def test_plot():
    _location_ = Path(__file__).resolve().parent
    with open(_location_ / "mock_data/df_pre_dissolve.pickle", "rb") as handle:
        streets_df = pickle.load(handle)

    plotting.plot(streets_df)
