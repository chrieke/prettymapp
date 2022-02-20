import pytest

from geopandas import GeoDataFrame

from prettybasicmaps.main import get_geometries
from prettybasicmaps.plotting import plot
from prettybasicmaps.settings import DRAW_SETTINGS


@pytest.mark.live
def test_get_geometries_live():
    df = get_geometries()
    assert isinstance(df, GeoDataFrame)


@pytest.mark.live
def test_main_live():
    df = get_geometries()
    fig = plot(df, drawing_kwargs=DRAW_SETTINGS)
    assert fig is not None
    #assert isinstance(fig, int)
    # import matplotlib.pyplot as plt
    # plt.show()
