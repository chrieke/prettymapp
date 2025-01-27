from fastapi import FastAPI, Query, HTTPException
from prettymapp.geo import get_aoi
from prettymapp.osm import get_osm_geometries
from prettymapp.plotting import Plot
from prettymapp.settings import STYLES
import tempfile
import os

app = FastAPI()

@app.get("/map_image")
def map_image(
    lat: float = Query(..., description="Latitude of the location"),
    lon: float = Query(..., description="Longitude of the location"),
    radius: int = Query(1000, description="Radius in meters"),
    style: str = Query("Peach", description="Style of the map")
):
    if style not in STYLES:
        raise HTTPException(status_code=400, detail="Invalid style parameter")

    try:
        aoi = get_aoi(coordinates=(lat, lon), radius=radius)
        df = get_osm_geometries(aoi)
        plot = Plot(df=df, aoi_bounds=aoi.bounds, draw_settings=STYLES[style])
        fig = plot.plot_all()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
            fig.savefig(tmpfile.name, format="png")
            image_url = f"/tmp/{os.path.basename(tmpfile.name)}"

        return {"image_url": image_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
