import logging
from typing import Optional
import time


from fastapi import FastAPI, HTTPException, Depends
from fastapi.logger import logger
from soknob import sonos
from soknob import config

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/volume/up")
def volume_up(settings: config.Settings = Depends(config.get_settings)):
    tic = time.perf_counter_ns()
    print("Volume Up")
    group = sonos.find_primary_group()
    if not group:
        logger.error("Could not find a primary group")
        raise HTTPException(status_code=400, detail="Could not find primary group")
    resp = sonos.group_volume_delta(group, settings.volume_up_delta)
    if resp.status_code != 200:
        logger.warn("Could not set volume")
    return resp.json()
     

@app.post("/volume/down")
def volume_down(settings: config.Settings = Depends(config.get_settings)):
    tic = time.perf_counter_ns()
    print("Volume Down")
    group = sonos.find_primary_group()
    if not group:
        logger.error("Could not find a primary group")
        raise HTTPException(status_code=400, detail="Could not find primary group")
    resp = sonos.group_volume_delta(group, settings.volume_down_delta)
    if resp.status_code != 200:
        logger.warn("Could not set volume")
    tock = time.perf_counter_ns()
    print("Time:", (tock-tic) / 1000000)
    return resp.json()

