import logging
from typing import Optional

from fastapi import FastAPI
from fastapi.logger import logger
from soknob import sonos

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/volume/up")
def volume_up():
    logger.warn("Volume Up")
    return {"volume": "up", "groups": sonos.get_groups()}

@app.post("/volume/down")
def volume_down():
    logger.warn("Volume Down")
    return {"volume": "down"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    return {"item_id": item_id, "q": q}
