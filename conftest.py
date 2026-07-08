import matplotlib
import pytest

# Non-interactive backend so plotting tests run headless (e.g. in CI)
matplotlib.use("Agg")


def pytest_addoption(parser):
    parser.addoption(
        "--runlive", action="store_true", default=False, help="run live tests"
    )


def pytest_collection_modifyitems(config, items):
    if not config.getoption("--runlive"):
        skip_live = pytest.mark.skip(reason="need --runlive option to run")
        for item in items:
            if "live" in item.keywords:
                item.add_marker(skip_live)
