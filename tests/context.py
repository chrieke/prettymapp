import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../prettybasicmaps")))

# Import the required classes and functions
# pylint: disable=unused-import,wrong-import-position
from prettybasicmaps.settings import LC_SETTINGS, DRAW_SETTINGS
from prettybasicmaps.main import main, query_osm
from prettybasicmaps.geo import validate_coordinates, get_aoi, adjust_street_width
from prettybasicmaps.plotting import plot

