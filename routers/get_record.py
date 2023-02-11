from collections import defaultdict
from datetime import datetime
from typing import Dict, Optional
from utils import get_average_status

from bson.son import SON
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import mongo_connection

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}},
)


class Sensor(BaseModel):
    """sensor data model"""
    gas_quantity: Optional[int]
    time: Optional[datetime]
    status: Optional[str]
    isCommand: bool
    isOpen: Optional[bool]

# TODO: every get method return a status of that gas in 3 function {x, y} status}


@router.get("/command")
def get_command() -> Dict[str, bool]:
    """get the status of the window

    Raises:
        HTTPException: if data is not found

    Returns:
        Dict: {"isOpen": bool}
    """
    rec = mongo_connection["Record"].find_one({"isCommand": True})
    if not rec:
        raise HTTPException(status_code=400, detail="Not detect yet")
    return {"isOpen": rec["isOpen"]}


@router.get("/last")
def last_quantity_status():
    """get last record of gas quantity and status

    Raises:
        HTTPException: when not have any record

    Returns:
        Dict["gas_quantity": float, "status": str] -- _description_
    """
    pipeline = [
        {"$sort": SON([("time", -1)])},
        {"$match": {"isCommand": False}},
        {"$limit": 1}
    ]
    record = mongo_connection["Record"].aggregate(pipeline).next()
    if not record:
        raise HTTPException(status_code=400, detail="Not detect yet")

    return {"gas_quantity": record["gas_quantity"], "status": record["status"]}


@router.get("/last_day")
def last_day_average():
    """get all record in the last day as list (interval of 1 hour)
    Raises:
        HTTPException: When record not found
    Returns:
        Dict["isCommand"] -- _description_
    """
    data = defaultdict(list)
    alldata = list(mongo_connection["Record"].find(
        {"isCommand": False}, {"_id": 0, "isCommand": 0}))

    if not alldata:
        raise HTTPException(status_code=400, detail='No record yet')
    limit = datetime.now().timestamp() - 24 * 3600
    for i in alldata:
        if i["time"].timestamp() > limit:
            date = i["time"]
            data[datetime(date.year, date.month,
                          date.day, date.hour)].append(i)
    result = {}
    status_count = defaultdict(int)
    total_count = 0
    for date, readings in data.items():
        result[date] = sum(
            map(lambda x: x["gas_quantity"], readings)) / len(readings)
        for reading in readings:
            status_count[reading["status"]] += 1
            total_count += 1
    avg_status = {
        status: count / total_count
        for status, count in status_count.items()
    }

    status_dct = {"SAFE": 0, "WARNING": 1, "DANGER": 2}
    status_sum = []
    for status, count in avg_status.items():
        if status in status_dct:
            status_sum.append(status_dct[status] * count)
    average_status = round(sum(status_sum) / total_count)
    average_status = list(status_dct.keys())[average_status]

    return [{"x": x, "y": y} for x, y in sorted(result.items(), key=lambda x: x[0])],{"s": average_status}



# get all record in the last hour
@router.get("/last_hour")
def last_hour():
    """get all record in the last hour as a list
    Raises:
        HTTPException: When record not found
    Returns:
        Dict["time", "gas_quantity" and "status"] -- _description_
    """
    data = []
    alldata = list(mongo_connection["Record"].find(
        {"isCommand": False}, {"_id": 0, "isCommand": 0}))
    limit = datetime.now().timestamp() - 3600
    if not alldata:
        raise HTTPException(status_code=400, detail='No record yet')
    for i in alldata:
        if i["time"].timestamp() > limit:
            temp = {
                "x": i["time"],
                "y": i["gas_quantity"],
                "s": i["status"]
            }
            data.append(temp)
    return data
    


@router.get("/all")
def all_time_average():
    """get all record all of data(average of day)

    Raises:
        HTTPException: When record not found

    Returns:
        Dict["isCommand"] -- _description_
    """
    data = defaultdict(list)
    alldata = list(mongo_connection["Record"].find(
        {"isCommand": False}, {"_id": 0, "gas_quantity": 0, "isCommand": 0}))

    if not alldata:
        raise HTTPException(status_code=400, detail='No record yet')

    for i in alldata:
        date = i["time"]
        data[datetime(date.year, date.month,
                      date.day)].append(i)
        result = {}
        status_count = defaultdict(int)
        total_count = 0
        for date, readings in data.items():
            sum_gas_quantity = 0
            for reading in readings:
                if "gas_quantity" in reading:
                    sum_gas_quantity += reading["gas_quantity"]
            result[date] = sum_gas_quantity / len(readings)
            for reading in readings:
                if "status" in reading:
                    status_count[reading["status"]] += 1
                    total_count += 1
    avg_status = {
        status: count / total_count
        for status, count in status_count.items()
    }

    status_dct = {"SAFE": 0, "WARNING": 1, "DANGER": 2}
    status_sum = []
    for status, count in avg_status.items():
        if status in status_dct:
            status_sum.append(status_dct[status] * count)

    average_status = round(sum(status_sum) / total_count)

    average_status = list(status_dct.keys())[average_status]

    return [{"x": x, "y": y} for x, y in sorted(result.items(), key=lambda x: x[0])],{"s": average_status}
    


