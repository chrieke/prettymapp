from prettymapp.plotting import adjust_lightness


def test_adjust_lightness():
    color = adjust_lightness("#FFC857")
    assert isinstance(color, tuple)
    assert len(color) == 3
    assert color == (0.6705882352941177, 0.4510504201680673, 0.0)
