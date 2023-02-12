from collections import defaultdict
from datetime import datetime
from typing import Dict, Optional
from utils import get_status

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
        {"$limit": 1},
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
    alldata = list(
        mongo_connection["Record"].find(
            {"isCommand": False}, {"_id": 0, "status": 0, "isCommand": 0}
        )
    )

    if not alldata:
        raise HTTPException(status_code=400, detail="No record yet")
    limit = datetime.now().timestamp() - 24 * 3600
    for i in alldata:
        if i["time"].timestamp() > limit:
            date = i["time"]
            data[datetime(date.year, date.month, date.day, date.hour)].append(
                i["gas_quantity"]
            )
    result = {}

    for date, readings in data.items():
        avg_gas = sum(map(lambda x: x[0], readings)) / len(readings)
        result[date] = [
            avg_gas,
            get_status(avg_gas),
        ]

    return [
        {"x": x, "y": y[0], "status": y[1]}
        for x, y in sorted(result.items(), key=lambda x: x[0])
    ]


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
    alldata = list(
        mongo_connection["Record"].find(
            {"isCommand": False}, {"_id": 0, "isCommand": 0}
        )
    )
    limit = datetime.now().timestamp() - 3600
    if not alldata:
        raise HTTPException(status_code=400, detail="No record yet")
    for i in alldata:
        if i["time"].timestamp() > limit:
            temp = {"x": i["time"], "y": i["gas_quantity"], "status": i["status"]}
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
    alldata = list(
        mongo_connection["Record"].find(
            {"isCommand": False}, {"_id": 0, "status": 0, "isCommand": 0}
        )
    )

    if not alldata:
        raise HTTPException(status_code=400, detail="No record yet")

    for i in alldata:
        date = i["time"]
        data[datetime(date.year, date.month, date.day)].append(i["gas_quantity"])
    result = {}

    for date, readings in data.items():
        avg_gas = sum(map(lambda x: x[0], readings)) / len(readings)
        result[date] = [
            avg_gas,
            get_status(avg_gas),
        ]

    return [
        {"x": x, "y": y[0], "status": y[1]}
        for x, y in sorted(result.items(), key=lambda x: x[0])
    ]
