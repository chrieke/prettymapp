import pytest

from .context import main


@pytest.mark.live
def test_main():
    fig = main()
    assert fig
    # import matplotlib.pyplot as plt
    # plt.show()
