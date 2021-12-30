import pytest
import matplotlib.pyplot as plt

from prettybasicmaps import main


@pytest.mark.live
def test_main():
    fig = main.main()
    assert fig
    #plt.show()
