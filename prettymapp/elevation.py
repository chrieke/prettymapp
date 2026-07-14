"""
Module for handling elevation/topography data including contour generation and hillshading.

Supports multiple elevation data sources:
- GEBCO (General Bathymetric Chart of the Oceans) - global coverage
- SRTM (Shuttle Radar Topography Mission) - 60°N to 60°S
- Local DEM files
"""

from typing import Optional, Tuple
import numpy as np
import rasterio
from rasterio.windows import Window
from shapely.geometry import Polygon, MultiPolygon, mapping
from geopandas import GeoDataFrame
from scipy.interpolate import griddata
from scipy import ndimage


class ElevationDataError(Exception):
    """Raised when elevation data cannot be retrieved or processed."""


def get_elevation_from_raster(
    bounds: Tuple[float, float, float, float],
    resolution: int = 100,
    data_source: str = "gebco",
) -> Tuple[np.ndarray, Tuple[float, float, float, float]]:
    """
    Fetch elevation data from a raster source within specified bounds.

    Args:
        bounds: (minx, miny, maxx, maxy) in EPSG:4326
        resolution: Number of pixels along longest dimension
        data_source: Source of elevation data ('gebco', 'srtm', or file path)

    Returns:
        Tuple of (elevation_array, bounds_in_data_crs)

    Raises:
        ElevationDataError: If data cannot be retrieved or processed
    """
    try:
        if data_source == "gebco":
            return _get_gebco_elevation(bounds, resolution)
        elif data_source == "srtm":
            return _get_srtm_elevation(bounds, resolution)
        else:
            # Treat as file path
            return _get_elevation_from_file(data_source, bounds, resolution)
    except Exception as e:
        raise ElevationDataError(
            f"Failed to retrieve elevation data from {data_source}: {str(e)}"
        ) from e


def _get_gebco_elevation(
    bounds: Tuple[float, float, float, float],
    resolution: int = 100,
) -> Tuple[np.ndarray, Tuple[float, float, float, float]]:
    """
    Fetch elevation data from GEBCO (requires local GEBCO file or online access).

    Note: This is a placeholder for integration with GEBCO data.
    Users should provide their own GEBCO NetCDF file or implement web service access.
    """
    raise ElevationDataError(
        "GEBCO support requires setting up GEBCO data. "
        "Download from https://www.gebco.net/ or use srtm/local file."
    )


def _get_srtm_elevation(
    bounds: Tuple[float, float, float, float],
    resolution: int = 100,
) -> Tuple[np.ndarray, Tuple[float, float, float, float]]:
    """
    Fetch elevation data from SRTM via rasterio/GDAL.

    Requires GDAL with VSI support for remote access.
    Coverage: 60°N to 60°S
    """
    minx, miny, maxx, maxy = bounds

    # Validate SRTM coverage
    if miny < -60 or maxy > 60:
        raise ElevationDataError(
            "SRTM data only available between 60°N and 60°S. "
            "Consider using GEBCO or a local DEM file instead."
        )

    try:
        # SRTM data via USGS
        dataset_url = "/vsicurl/https://cloud.sdsc.edu/v1/AUTH_ogc/Raster/SRTM_GL30/SRTM_GL30.vrt"

        with rasterio.open(dataset_url) as src:
            window = rasterio.windows.from_bounds(minx, miny, maxx, maxy, src.transform)
            elevation_data = src.read(1, window=window)

        return elevation_data, bounds
    except Exception as e:
        raise ElevationDataError(
            f"Could not fetch SRTM data. Ensure GDAL is configured. Error: {str(e)}"
        ) from e


def _get_elevation_from_file(
    filepath: str,
    bounds: Tuple[float, float, float, float],
    resolution: int = 100,
) -> Tuple[np.ndarray, Tuple[float, float, float, float]]:
    """
    Load elevation data from a local GeoTIFF or other raster file.

    Args:
        filepath: Path to raster file (GeoTIFF recommended)
        bounds: (minx, miny, maxx, maxy) query bounds in file's CRS
        resolution: Target resolution

    Returns:
        Tuple of (elevation_array, bounds)
    """
    with rasterio.open(filepath) as src:
        try:
            window = rasterio.windows.from_bounds(
                bounds[0], bounds[1], bounds[2], bounds[3], src.transform
            )
            elevation_data = src.read(1, window=window)
            return elevation_data, bounds
        except Exception as e:
            raise ElevationDataError(
                f"Could not read elevation data from {filepath}: {str(e)}"
            ) from e


def generate_hillshade(
    elevation: np.ndarray,
    azimuth: float = 315,
    altitude: float = 45,
    normalize: bool = True,
) -> np.ndarray:
    """
    Generate hillshade from elevation data.

    Creates a 3D-like shaded relief effect by calculating lighting based on
    surface normals.

    Args:
        elevation: 2D elevation array
        azimuth: Light direction in degrees (0-360, 0=North)
        altitude: Light angle above horizon in degrees (0-90)
        normalize: Whether to normalize output to 0-255 range

    Returns:
        Hillshade as 2D numpy array (0-255 if normalized, 0-1 otherwise)
    """
    azimuth_rad = np.radians(azimuth)
    altitude_rad = np.radians(altitude)

    # Calculate gradients
    x, y = np.gradient(elevation)

    # Calculate normal vectors
    normal = np.dstack((-x, -y, np.ones_like(elevation)))
    norm = np.linalg.norm(normal, axis=2)
    normal = normal / norm[:, :, np.newaxis]

    # Light vector
    light_vector = np.array([
        np.cos(altitude_rad) * np.sin(azimuth_rad),
        np.cos(altitude_rad) * np.cos(azimuth_rad),
        np.sin(altitude_rad),
    ])

    # Lambertian reflection
    hillshade = np.dot(normal, light_vector)
    hillshade = np.clip(hillshade, 0, 1)

    if normalize:
        hillshade = (hillshade * 255).astype(np.uint8)

    return hillshade


def generate_contours(
    elevation: np.ndarray,
    bounds: Tuple[float, float, float, float],
    interval: Optional[int] = None,
    min_elevation: Optional[float] = None,
    max_elevation: Optional[float] = None,
) -> GeoDataFrame:
    """
    Generate contour lines from elevation data.

    Args:
        elevation: 2D elevation array
        bounds: (minx, miny, maxx, maxy) in geographic coordinates
        interval: Contour interval in meters. If None, auto-calculated.
        min_elevation: Minimum elevation to include (default: min of data)
        max_elevation: Maximum elevation to include (default: max of data)

    Returns:
        GeoDataFrame with contour linestrings and elevation values
    """
    try:
        from matplotlib import pyplot as plt
    except ImportError:
        raise ElevationDataError(
            "matplotlib required for contour generation. "
            "Install with: pip install matplotlib"
        )

    minx, miny, maxx, maxy = bounds
    min_elev = min_elevation or np.nanmin(elevation)
    max_elev = max_elevation or np.nanmax(elevation)

    # Auto-calculate interval if not provided
    if interval is None:
        elev_range = max_elev - min_elev
        interval = max(10, int(elev_range / 10))  # ~10 contours

    # Create coordinate grids
    x = np.linspace(minx, maxx, elevation.shape[1])
    y = np.linspace(miny, maxy, elevation.shape[0])
    X, Y = np.meshgrid(x, y)

    # Generate contours
    contours = plt.contour(
        X, Y, elevation, levels=np.arange(min_elev, max_elev + interval, interval)
    )

    # Extract contour data
    geometries = []
    elevations = []

    for contour_collection in contours.collections:
        for path in contour_collection.get_paths():
            vertices = path.vertices
            if len(vertices) > 1:
                from shapely.geometry import LineString

                geometries.append(LineString(vertices))

    # Get elevation levels from contour labels
    for i, level in enumerate(contours.levels):
        elevations.append(level)

    plt.close()

    if not geometries:
        raise ElevationDataError("No contours could be generated from elevation data.")

    # Create GeoDataFrame
    df = GeoDataFrame(
        {
            "geometry": geometries,
            "elevation": [contours.levels[i % len(contours.levels)] for i in range(len(geometries))],
        },
        crs="EPSG:4326",
    )

    return df


def calculate_slope(elevation: np.ndarray) -> np.ndarray:
    """
    Calculate slope in degrees from elevation data.

    Args:
        elevation: 2D elevation array

    Returns:
        2D slope array in degrees
    """
    x, y = np.gradient(elevation)
    slope = np.degrees(np.arctan(np.sqrt(x**2 + y**2)))
    return slope


def calculate_aspect(elevation: np.ndarray) -> np.ndarray:
    """
    Calculate aspect (direction of slope) in degrees from elevation data.

    Args:
        elevation: 2D elevation array

    Returns:
        2D aspect array in degrees (0-360, 0=North, 90=East, etc.)
    """
    x, y = np.gradient(elevation)
    aspect = np.degrees(np.arctan2(-x, y))
    aspect = np.where(aspect < 0, aspect + 360, aspect)
    return aspect
