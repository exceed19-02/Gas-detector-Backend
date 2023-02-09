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


@router.get("/command")
def get_command():
    rec = mongo_connection["Record"].find_one({"isCommand": True})
    if not rec:
        raise HTTPException(status_code=400, detail="Not detect yet")
    else:
        return {"isOpen": rec["isOpen"]}


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
