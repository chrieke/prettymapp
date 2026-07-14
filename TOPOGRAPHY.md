# Topography & Elevation Features

This document explains how to use the new topography features in prettymapp to create beautiful maps with elevation contours and hillshading effects.

## Quick Start

### Basic Usage with Contours

```python
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.topography import apply_topography_overlay, TopographySettings
from prettymapp.settings import STYLES

# Get area of interest (e.g., Swiss Alps)
aoi = get_aoi(address="Swiss Alps", radius=5000)

# Get OSM data
osm_gdf = get_osm_geometries(aoi)

# Create base map
plot = Plot(osm_gdf, aoi.bounds, draw_settings=STYLES["Peach"])
fig = plot.plot_all()

# Add topographic contours
topo_settings = TopographySettings(
    show_contours=True,
    show_hillshading=False,
    contour_color="#1a1a1a",
    contour_linewidth=0.7
)
apply_topography_overlay(
    plot.ax,
    aoi.bounds,
    settings=topo_settings,
    elevation_source="srtm"
)

# Display
import matplotlib.pyplot as plt
plt.show()
```

### Hillshading Only

```python
from prettymapp.topography import TopographySettings, apply_topography_overlay

# Create subtle hillshading overlay
topo_settings = TopographySettings(
    show_contours=False,
    show_hillshading=True,
    hillshade_alpha=0.25,
    hillshade_cmap="gray"
)

apply_topography_overlay(
    plot.ax,
    aoi.bounds,
    settings=topo_settings,
    elevation_source="srtm"
)
```

### Combined Topographic Map (Contours + Hillshading)

```python
from prettymapp.settings import TOPOGRAPHY_STYLES

# Use pre-configured "Topographic" style
topo_config = TOPOGRAPHY_STYLES["Topographic"]
topo_settings = TopographySettings(**topo_config)

apply_topography_overlay(
    plot.ax,
    aoi.bounds,
    settings=topo_settings,
    elevation_source="srtm"
)
```

## Configuration Options

### TopographySettings Parameters

```python
@dataclass
class TopographySettings:
    # Contour settings
    show_contours: bool = True              # Display elevation contours
    contour_interval: Optional[int] = None  # Meters between contours (auto if None)
    contour_color: str = "#666666"          # Hex color for contour lines
    contour_linewidth: float = 0.5          # Width of contour lines
    contour_zorder: int = 5                 # Drawing order (higher = on top)
    
    # Major contours (emphasis every N meters)
    major_contour_interval: Optional[int] = None
    major_contour_linewidth: float = 1.5    # Width multiplier for major contours
    
    # Hillshading settings
    show_hillshading: bool = False          # Apply shaded relief effect
    hillshade_alpha: float = 0.3            # Transparency (0=invisible, 1=opaque)
    hillshade_azimuth: float = 315          # Light direction (degrees, 0=N, 90=E)
    hillshade_altitude: float = 45          # Light angle above horizon (0-90)
    hillshade_cmap: str = "gray"            # Colormap ('gray', 'terrain', etc.)
```

## Elevation Data Sources

### SRTM (Shuttle Radar Topography Mission)
- **Coverage**: 60°N to 60°S
- **Resolution**: 30 meters
- **Best for**: Most populated regions
- **Setup**: Requires GDAL with VSI support
- **Usage**: `elevation_source="srtm"`

```python
# Requires GDAL installation:
# conda install gdal
# or
# brew install gdal

apply_topography_overlay(
    plot.ax, aoi.bounds,
    elevation_source="srtm"
)
```

### Local DEM Files
- **Format**: GeoTIFF or other raster formats supported by rasterio
- **Coverage**: User-defined
- **Resolution**: User-defined
- **Best for**: Polar regions or high-resolution data
- **Usage**: `elevation_source="/path/to/dem.tif"`

```python
# Use local DEM file
apply_topography_overlay(
    plot.ax, aoi.bounds,
    elevation_source="/data/arctic_dem.tif"
)
```

### GEBCO (General Bathymetric Chart of the Oceans)
- **Coverage**: Global, including bathymetry
- **Best for**: Ocean areas, global coverage
- **Status**: Placeholder (requires setup)
- **Setup**: Download from https://www.gebco.net/

```python
# Future: After setting up GEBCO data
# apply_topography_overlay(
#     plot.ax, aoi.bounds,
#     elevation_source="gebco"
# )
```

## Pre-configured Styles

Three topography presets are available in `settings.TOPOGRAPHY_STYLES`:

### Contours Style
```python
from prettymapp.settings import TOPOGRAPHY_STYLES
from prettymapp.topography import TopographySettings

config = TOPOGRAPHY_STYLES["Contours"]
# Auto-calculates interval, dark lines, contours only
```

### Hillshade Style
```python
config = TOPOGRAPHY_STYLES["Hillshade"]
# Subtle gray hillshading, no contours
```

### Topographic Style
```python
config = TOPOGRAPHY_STYLES["Topographic"]
# Full topographic map: contours every 100m, 
# major contours every 500m, hillshading overlay
```

## Advanced Usage

### Custom Contour Intervals

```python
# Mountain map with detailed contours
topo_settings = TopographySettings(
    show_contours=True,
    contour_interval=50,           # Contour every 50 meters
    major_contour_interval=250,    # Emphasize every 250m
    contour_color="#8B6914",       # Brown color
    contour_linewidth=0.6,
    major_contour_linewidth=1.8
)
```

### Directional Lighting

```python
# Change light direction for different effect
topo_settings = TopographySettings(
    show_hillshading=True,
    hillshade_azimuth=270,   # Light from West
    hillshade_altitude=30,   # Lower angle for stronger shadows
    hillshade_alpha=0.4
)
```

### Pre-computed Elevation Data

```python
from prettymapp.elevation import get_elevation_from_raster

# Fetch elevation data separately
elevation, bounds = get_elevation_from_raster(
    aoi.bounds,
    data_source="srtm"
)

# Can reuse for multiple plots
apply_topography_overlay(
    plot.ax,
    aoi.bounds,
    elevation=elevation,  # Pass pre-computed data
    settings=topo_settings
)
```

### Elevation Analysis

```python
from prettymapp.elevation import calculate_slope, calculate_aspect

# Get elevation data
elevation, _ = get_elevation_from_raster(aoi.bounds, data_source="srtm")

# Calculate terrain properties
slope = calculate_slope(elevation)
aspect = calculate_aspect(elevation)

# Use for further analysis
steep_areas = slope > 30  # Areas steeper than 30°
```

## Integration with Map Styles

Topography works well with different base map styles:

```python
from prettymapp.settings import STYLES, TOPOGRAPHY_STYLES
from prettymapp.topography import TopographySettings

# Combine base style with topography
plot = Plot(osm_gdf, aoi.bounds, draw_settings=STYLES["Auburn"])

# Add topography
topo_config = TOPOGRAPHY_STYLES["Topographic"]
topo_settings = TopographySettings(**topo_config)

apply_topography_overlay(plot.ax, aoi.bounds, settings=topo_settings)
```

## Error Handling

The topography system gracefully handles errors:

```python
# Will warn if SRTM is unavailable, continue without topography
try:
    apply_topography_overlay(plot.ax, aoi.bounds, elevation_source="srtm")
except ElevationDataError as e:
    print(f"Elevation data unavailable: {e}")
    # Map still displays without topographic features
```

## Performance Considerations

- **Contour generation**: ~1-3 seconds for typical map sizes
- **Hillshading**: ~0.5-1 second
- **Memory**: Elevation arrays ~10-50MB depending on resolution
- **SRTM access**: First access requires download (~5-10MB), then cached locally

## Requirements

### Core Dependencies
```
rasterio>=1.3.0
scipy>=1.10.0
```

### Optional (for SRTM access)
```
gdal>=3.0  # System package or conda
```

### Installation
```bash
# Minimal (local DEM only)
pip install rasterio scipy

# Full (including SRTM support)
conda install gdal
pip install rasterio scipy

# Or with uv
uv pip install rasterio scipy
```

## Troubleshooting

### "Could not fetch SRTM data"
- Ensure GDAL is installed: `conda install gdal`
- Check internet connection
- Try using a local DEM file instead

### "matplotlib required for contour generation"
- Install matplotlib: `pip install matplotlib`

### "No contours could be generated"
- Check that elevation data contains valid values
- Verify bounds are within data coverage area
- Try adjusting contour_interval

### Performance Issues
- Reduce map size (use smaller radius)
- Use lower resolution DEM
- Disable hillshading if not needed

## Examples by Region

### Alpine Region (Swiss Alps)
```python
aoi = get_aoi(address="Zermatt, Switzerland", radius=8000)
config = TOPOGRAPHY_STYLES["Topographic"]
# Major contours every 500m, minor every 100m
```

### Volcanic Region (Mt. Fuji)
```python
aoi = get_aoi(address="Mt. Fuji, Japan", radius=10000)
config = TOPOGRAPHY_STYLES["Contours"]
config["contour_color"] = "#8B4513"  # Brown
```

### Coastal Region
```python
# Use local DEM with bathymetry data
apply_topography_overlay(
    plot.ax, aoi.bounds,
    elevation_source="coastal_dem.tif"
)
```

## Future Enhancements

Planned features:
- [ ] GEBCO integration for global bathymetric maps
- [ ] Slope-based coloring
- [ ] 3D elevation visualization
- [ ] Aspect-shaded relief
- [ ] Multiple elevation sources in single map

## References

- [SRTM Data](https://lpdaac.usgs.gov/products/srtmgl1v003/)
- [GEBCO](https://www.gebco.net/)
- [Rasterio Documentation](https://rasterio.readthedocs.io/)
- [Hillshading Algorithm](https://en.wikipedia.org/wiki/Shaded_relief)
