from typing import Optional
from fastapi import FastAPI
from typing import List
from starlette.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from helpers.get_property_coordinates import get_property_coordinates
from helpers.convertors import lkm92tm_to_geodetic

app = FastAPI()

app.mount("/public", StaticFiles(directory="static/public"), name="public")


@app.get("/")
def frontend():
    return RedirectResponse(url="/public/index.html")


@app.get("/get_property_coordinates")
async def url_get_property_coordinates(cadastre_code: str) -> List[List]:
    lkm92tm_property_rings = await get_property_coordinates(cadastre_code)
    geodetic_property_rings = []
    for lkm92tm_property_ring in lkm92tm_property_rings:
        geodetic_ring = []
        for lkm92tm_coordinate in lkm92tm_property_ring:
            geodetic_ring.append(lkm92tm_to_geodetic(lkm92tm_coordinate[1], lkm92tm_coordinate[0]))
        geodetic_property_rings.append(geodetic_ring)
    return geodetic_property_rings


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
