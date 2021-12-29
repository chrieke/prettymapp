import pytest
import matplotlib.pyplot as plt

from prettybasicmaps import main


@pytest.mark.live
def test_main():
    ax = main.main()
    assert ax
    plt.show()
