from typing import Optional
from fastapi import FastAPI
import uvicorn

from helpers.get_property_coordinates import get_property_coordinates

app = FastAPI()


@app.get("/get_property_coordinates")
def url_get_property_coordinates(cadastre_code: str):
    return get_property_coordinates(cadastre_code)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
