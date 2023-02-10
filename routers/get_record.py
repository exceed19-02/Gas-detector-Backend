from fastapi import APIRouter, Body, HTTPException
from typing import Union, Optional
from pydantic import BaseModel
from datetime import date, datetime
from database import mongo_connection
from bson.son import SON

router = APIRouter(
    prefix="/record",
    tags=["record"],
    responses={404: {"description": "Not found"}},
)


class Sensor(BaseModel):
    gas_quantity: Optional[int]
    time: Optional[datetime]
    status: Optional[str]
    isCommand: bool
    isOpen: Optional[bool]

# get status of the window
@router.get("/command")
def get_command():
    rec = mongo_connection["Record"].find_one({"isCommand": True})
    if not rec:
        raise HTTPException(status_code=400, detail="Not detect yet")
    else:
        return {"isOpen": rec["isOpen"]}

# get last record
@router.get("/last")
def last_quantity_status():
    pipeline = [
        {"$sort": SON([("time", -1)])},
        {"$match": {"isCommand": False}},
        {"$limit": 1}
    ]
    record = mongo_connection["Record"].aggregate(pipeline).next()
    if not record:
        raise HTTPException(status_code=400, detail="Not detect yet")
    else:
        return {"gas_quantity": record["gas_quantity"], "status": record["status"]}

# get all data in the last hour
@router.get("/last_hour")
def last_hour():
    data = []
    alldata = list(mongo_connection["Record"].find({"isCommand": False}, {"_id": 0, "status": 0, "isCommand": 0}))
    limit = datetime.now().timestamp() - 3600
    for i in alldata:
        if i["time"].timestamp() > limit:
            temp = {
                "x": i["time"],
                "y": i["gas_quantity"]
            }
            data.append(temp)
    return data