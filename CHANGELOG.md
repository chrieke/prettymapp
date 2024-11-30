# Changelog

Update your installation to the latest version:

=== "pip"

    ```bash
    # pip show prettymapp  # check currently installed version
    pip install prettymapp --upgrade
    ```

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
