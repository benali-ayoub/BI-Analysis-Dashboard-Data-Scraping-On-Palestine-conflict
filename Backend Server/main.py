from typing import Union
from fastapi import FastAPI

from get_countries import download_countries_data
from update_demographics import get_demographics_data
from update_fatalities import get_fatalities_data
from update_live_statistics import get_stats_data
from update_prisonners import get_prisoners_data
from update_refugees import get_refugees_data
from update_settlements import get_settlements_data

app = FastAPI()


@app.get("/")
def read_root():
    return {"BI Project": "Master SD - Projet SAD 2023"}


@app.get("/get_countries")
async def get_countries_data():
    download_countries_data()
    return {"status": "Data downloaded"}

@app.get("/update_refugees")
async def update_refugees_data():
    get_refugees_data()
    return {"status": "Data updated"}

@app.get("/update_demographics")
async def update_demographics_data():
    get_demographics_data()
    return {"status": "Data updated"}

@app.get("/update_prisoners")
async def update_prisoners_data():
    await get_prisoners_data()
    return {"status": "Data updated"}

@app.get("/update_fatalities")
async def update_fatalities_data():
    await get_fatalities_data()
    return {"status": "Data updated"}

@app.get("/update_settlements")
async def update_settlements_data():
    await get_settlements_data()
    return {"status": "Data updated"}

@app.get("/update_stats")
async def update_stats_data():
    await get_stats_data()
    return {"status": "Data updated"}