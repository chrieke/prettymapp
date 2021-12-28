import pytest
from geopandas import GeoDataFrame

from prettiermaps import main


@pytest.mark.live
def test_main():
    df = main.main()
    assert isinstance(df, GeoDataFrame)
