# Changelog

Update your installation to the latest version:

=== "pip"

    ```bash
    # pip show prettymapp  # check currently installed version
    pip install prettymapp --upgrade
    ```

## 0.7.0
**unreleased**

- Adds `OsmDataError` and clearer error handling for empty areas and failed geocoding / OSM
  downloads (raises instead of returning empty or crashing).
- Replaces private `geopandas.plotting` functions with public matplotlib collections, and uses
  the stable top-level `osmnx` API instead of submodule imports - avoids breakage on dependency
  upgrades.
- New `dpi` parameter on `Plot` (default 300, previously hardcoded 1200) for much faster, lower-
  memory rendering.
- Building colors are now seeded, so identical inputs render identical maps.
- Fixes an invalid edge color in the `Flannel` streets style.
- Other: osmnx 2.0 data handling, `osmnx<3` bound with `geopandas`/`shapely` as direct
  dependencies, faster `explode_multigeometries`, and various test & tooling fixes.

## 0.6.0
**December 25, 2025**

- Add image download button with format (png, svg) selection
- Small improvements to local run config


## 0.5.0
**December 29, 2024**

- Adds boolean `credits` parameter to the `Plot` class. Set to `False` to hide the OSM/package credits on the map.
- Fixes an issue where customized landcover_classes where ignored in `get_osm_geometries`.
- Fixes an issue where setting a landcover_class to `False` resulted in a Keyerror.
- Various documentation & example improvements.

## 0.4.0
**November 30, 2024**

- Allow selection of landcover classes via new `landcover_classes` parameter in `get_osm_geometries`
- `drawing_settings` parameter in `Plot` now defaults to `STYLES["Peach"]`
- `pyproject.toml` replaces setup.py & requirements.txt files

## 0.3.0
**April 23, 2024**

- Add get_osm_geometries_from_xml to plot OSM XML files
- Add Dockerfile


## 0.2.0
**August 25, 2023**

- Upgraded dependencies, adjust deprecated functions.

## 0.1.0
**December 03, 2022**

- Initial stable release on pypi
