"""
Integration of topographic features (contours, hillshading) into prettymapp plots.

Provides utilities to overlay elevation-based features on existing maps.
"""

from dataclasses import dataclass
from typing import Optional, Tuple
import numpy as np
from geopandas import GeoDataFrame
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt

from prettymapp.elevation import (
    generate_hillshade,
    generate_contours,
    ElevationDataError,
)


@dataclass
class TopographySettings:
    """Configuration for topographic map overlays.

    Attributes:
        show_contours: Whether to display elevation contours
        show_hillshading: Whether to apply hillshade relief
        contour_interval: Elevation interval between contour lines in meters
        contour_color: Color of contour lines (hex or matplotlib color)
        contour_linewidth: Width of contour lines
        contour_zorder: Z-order for contour rendering
        hillshade_alpha: Transparency of hillshade overlay (0-1)
        hillshade_azimuth: Light direction in degrees (0-360)
        hillshade_altitude: Light angle above horizon (0-90)
        hillshade_cmap: Colormap for hillshade ('gray', 'terrain', etc.)
        major_contour_interval: Interval for emphasized contours (optional)
        major_contour_linewidth: Width multiplier for major contours
    """

    show_contours: bool = True
    show_hillshading: bool = False
    contour_interval: Optional[int] = None  # Auto-calculate if None
    contour_color: str = "#666666"
    contour_linewidth: float = 0.5
    contour_zorder: int = 5
    hillshade_alpha: float = 0.3
    hillshade_azimuth: float = 315
    hillshade_altitude: float = 45
    hillshade_cmap: str = "gray"
    major_contour_interval: Optional[int] = None
    major_contour_linewidth: float = 1.5


def add_hillshading(
    ax,
    elevation: np.ndarray,
    bounds: Tuple[float, float, float, float],
    settings: TopographySettings,
) -> None:
    """
    Apply hillshade relief to map axes.

    Args:
        ax: Matplotlib axes object
        elevation: 2D elevation array
        bounds: (minx, miny, maxx, maxy) geographic bounds
        settings: TopographySettings configuration
    """
    try:
        hillshade = generate_hillshade(
            elevation,
            azimuth=settings.hillshade_azimuth,
            altitude=settings.hillshade_altitude,
        )

        minx, miny, maxx, maxy = bounds
        extent = [minx, maxx, miny, maxy]

        ax.imshow(
            hillshade,
            extent=extent,
            cmap=settings.hillshade_cmap,
            alpha=settings.hillshade_alpha,
            zorder=settings.contour_zorder - 1,
            aspect="auto",
        )
    except Exception as e:
        print(f"Warning: Could not apply hillshading: {str(e)}")


def add_contours(
    ax,
    elevation: np.ndarray,
    bounds: Tuple[float, float, float, float],
    settings: TopographySettings,
) -> None:
    """
    Draw elevation contour lines on map axes.

    Args:
        ax: Matplotlib axes object
        elevation: 2D elevation array
        bounds: (minx, miny, maxx, maxy) geographic bounds
        settings: TopographySettings configuration
    """
    try:
        contours_gdf = generate_contours(
            elevation, bounds, interval=settings.contour_interval
        )

        if contours_gdf.empty:
            return

        # Handle major contours if specified
        if settings.major_contour_interval:
            major_mask = (
                contours_gdf["elevation"] % settings.major_contour_interval == 0
            )
            minor_contours = contours_gdf[~major_mask]
            major_contours = contours_gdf[major_mask]

            # Draw minor contours
            for idx, row in minor_contours.iterrows():
                geom = row.geometry
                coords = np.array(geom.coords)
                ax.plot(
                    coords[:, 0],
                    coords[:, 1],
                    color=settings.contour_color,
                    linewidth=settings.contour_linewidth,
                    zorder=settings.contour_zorder,
                    alpha=0.6,
                )

            # Draw major contours
            for idx, row in major_contours.iterrows():
                geom = row.geometry
                coords = np.array(geom.coords)
                ax.plot(
                    coords[:, 0],
                    coords[:, 1],
                    color=settings.contour_color,
                    linewidth=settings.contour_linewidth * settings.major_contour_linewidth,
                    zorder=settings.contour_zorder,
                )
        else:
            # Draw all contours uniformly
            for idx, row in contours_gdf.iterrows():
                geom = row.geometry
                coords = np.array(geom.coords)
                ax.plot(
                    coords[:, 0],
                    coords[:, 1],
                    color=settings.contour_color,
                    linewidth=settings.contour_linewidth,
                    zorder=settings.contour_zorder,
                )

    except ElevationDataError as e:
        print(f"Warning: Could not generate contours: {str(e)}")
    except Exception as e:
        print(f"Warning: Error drawing contours: {str(e)}")


def apply_topography_overlay(
    ax,
    aoi_bounds: Tuple[float, float, float, float],
    elevation: Optional[np.ndarray] = None,
    settings: Optional[TopographySettings] = None,
    elevation_source: str = "gebco",
) -> None:
    """
    Apply topographic overlays to an existing map.

    This is the main entry point for adding topography to prettymapp plots.

    Args:
        ax: Matplotlib axes object (from Plot.ax)
        aoi_bounds: (minx, miny, maxx, maxy) geographic bounds
        elevation: Pre-computed elevation array (if None, will be fetched)
        settings: TopographySettings configuration (uses defaults if None)
        elevation_source: Source for elevation data ('gebco', 'srtm', or file path)

    Example:
        ```python
        from prettymapp.plotting import Plot
        from prettymapp.topography import apply_topography_overlay, TopographySettings

        plot = Plot(df, aoi_bounds, draw_settings=STYLES["Peach"])
        fig = plot.plot_all()

        topo_settings = TopographySettings(
            show_contours=True,
            show_hillshading=True,
            contour_color="#1a1a1a"
        )
        apply_topography_overlay(
            plot.ax,
            aoi_bounds,
            settings=topo_settings,
            elevation_source="srtm"
        )
        ```
    """
    if settings is None:
        settings = TopographySettings()

    try:
        # Fetch elevation if not provided
        if elevation is None:
            from prettymapp.elevation import get_elevation_from_raster

            elevation, _ = get_elevation_from_raster(
                aoi_bounds, data_source=elevation_source
            )

        # Apply hillshading
        if settings.show_hillshading:
            add_hillshading(ax, elevation, aoi_bounds, settings)

        # Draw contours
        if settings.show_contours:
            add_contours(ax, elevation, aoi_bounds, settings)

    except ElevationDataError as e:
        print(f"Topography overlay failed: {str(e)}")
        print("Map will be displayed without topographic features.")
    except Exception as e:
        print(f"Unexpected error in topography overlay: {str(e)}")
