import pytest
from geopandas import GeoDataFrame

from prettymapp.main import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES


@pytest.mark.live
def test_get_geometries_live():
    df = get_osm_geometries()
    assert isinstance(df, GeoDataFrame)


@pytest.mark.live
def test_main_live():
    df = get_osm_geometries()
    fig = Plot(df=df, draw_settings=STYLES["Peach"]).plot_all()
    assert fig is not None
    # assert isinstance(fig, int)
    # import matplotlib.pyplot as plt
    # plt.show()
