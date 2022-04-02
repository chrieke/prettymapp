# prettymapp 🖼️

**Prettymapp is a webapp to create beautiful maps from OpenStreetMap data (based on prettymaps)**

---
<h3 align="center">
    🎈 Try it out here: <a href="https://share.streamlit.io/chrieke/prettymapp/main/streamlit-prettymapp/app.
py">prettymapp on streamlit 🎈 </a>
</h3>

---



<p align="center">
    <a href="https://share.streamlit.io/chrieke/prettymapp/main/streamlit-prettymapp/app.
py"><img src="./streamlit-prettymapp/example_prints/demo.gif" width=700></a>
</p>

<br>

<table>
    <tr><td><img src="./streamlit-prettymapp/example_prints/macau.png"></td><td><img src="./streamlit-prettymapp/example_prints/barcelona.png"></td></tr>
</table>

## Based on the prettymaps project

Prettymapp is based on a rewrite of the fantastic [prettymaps](https://github.com/marceloprates/prettymaps) project by
[@marceloprates](https://github.com/marceloprates). All credit for the original idea, designs and implementation go to him.
The prettymapp rewrite focuses on speed and adapted configuration to interface with the webapp.
It drops more complex configuration options in favour of improved speed, reduced code complexity and 
simplified configuration interfaces. It is partially tested and adds a [streamlit](https://streamlit.io/) webapp component.

## Standalone Python package

In addition to the [streamlit webapp](https://share.streamlit.io/chrieke/prettymapp/main/streamlit-prettymapp/app.py), 
you can also use the Python package to create your own application or further customize the functionality.

**Installation:**

```bash
pip install git+https://github.com/chrieke/prettymapp.git
```

**Define the area, download and plot the osm data:**

```python
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES

aoi = get_aoi(address="Brandenburger Tor, Berlin", distance=500, rectangular=True)
df = get_osm_geometries(aoi=aoi)

fig = Plot(
    df=df,
    aoi_bounds=aoi.bounds,
    draw_settings=STYLES["Peach"]
).plot_all()
```

To customize the map apperance, use the additional arguments of the 
[`Plot`](https://github.com/chrieke/prettymapp/blob/5c4b7976711a5a2a01c5aa3b113dba299180e95c/prettymapp/plotting.py#L36) 
class (e.g. `shape`, `contour_width` etc.).
Check the preconfigured [styles](https://github.com/chrieke/prettymapp/blob/5c4b7976711a5a2a01c5aa3b113dba299180e95c/prettymapp/settings.py#L35)
and webapp [examples](https://github.com/chrieke/prettymapp/blob/main/streamlit-prettymapp/examples.py) for 
inspiration.



