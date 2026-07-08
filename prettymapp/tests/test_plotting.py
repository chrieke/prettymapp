from pathlib import Path

import numpy as np
from matplotlib.pyplot import close

from prettymapp.osm import get_osm_geometries_from_xml
from prettymapp.plotting import Plot, adjust_lightness
from prettymapp.settings import STYLES

MOCK_XML = Path(__file__).parent / "mock_data" / "osm_export_xml.osm"


def test_adjust_lightness():
    color = adjust_lightness("#FFC857")
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert color == (0.6705882352941177, 0.4510504201680673, 0.0)


def test_plot_all_offline():
    df = get_osm_geometries_from_xml(MOCK_XML)
    fig = Plot(
        df=df,
        aoi_bounds=list(df.total_bounds),
        draw_settings=STYLES["Peach"],
        name_on=True,
        name="mock",
        contour_width=2,
        credits=True,
    ).plot_all()

    assert fig is not None
    ax = fig.axes[0]
    # Geometries were drawn as collections, text (title + credits) was added
    assert len(ax.collections) > 0
    assert len(ax.texts) == 2
    close(fig)


def test_plot_all_is_deterministic():
    """Identical input renders identical maps (seeded cmap values)."""
    df = get_osm_geometries_from_xml(MOCK_XML)

    def cmap_arrays(fig):
        return [
            c.get_array() for c in fig.axes[0].collections if c.get_array() is not None
        ]

    fig1 = Plot(df=df, aoi_bounds=list(df.total_bounds)).plot_all()
    fig2 = Plot(df=df, aoi_bounds=list(df.total_bounds)).plot_all()
    arrays1, arrays2 = cmap_arrays(fig1), cmap_arrays(fig2)
    assert arrays1
    for a1, a2 in zip(arrays1, arrays2):
        np.testing.assert_array_equal(a1, a2)
    close(fig1)
    close(fig2)
