from prettymapp.plotting import adjust_lightness, Plot
from shapely.geometry import LineString
import geopandas as gpd
import matplotlib.pyplot as plt


def test_adjust_lightness():
    color = adjust_lightness("#FFC857")
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert color == (0.6705882352941177, 0.4510504201680673, 0.0)


def test_set_street_names():
    # Create a simple GeoDataFrame with street geometries and names
    data = {
        "geometry": [LineString([(0, 0), (1, 1)]), LineString([(1, 1), (2, 2)])],
        "landcover_class": ["streets", "streets"],
        "highway": ["residential", "residential"],
        "name": ["Street 1", "Street 2"],
    }
    df = gpd.GeoDataFrame(data)

    # Create a Plot object
    plot = Plot(
        df=df,
        aoi_bounds=[0, 0, 2, 2],
        draw_settings={"streets": {"fc": "#2F3737", "zorder": 3}},
        name_on=False,
        font_size=10,
        font_color="#2F3737",
    )

    # Plot the street names
    plot.set_street_names()

    # Check if the street names are rendered correctly
    fig = plot.fig
    ax = plot.ax
    texts = [text.get_text() for text in ax.texts]
    assert "Street 1" in texts
    assert "Street 2" in texts

    # Display the plot (optional, for visual inspection)
    plt.show()
