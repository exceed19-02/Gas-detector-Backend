from fastapi import APIRouter, Body, HTTPException
from typing import Union, Optional
from pydantic import BaseModel
from datetime import date, datetime
from database import mongo_connection

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


# @router.get("/")
# def last():
#     last_rec = mongo_connection["Record"].find({})
#
@router.get("/last")
def last_quantity_status():
    last_rec = mongo_connection["Record"].find().sort({"time": -1}).limit(1)
    print(list(last_rec))
    # if not last_rec:
    #     raise HTTPException(status_code=400, detail="Not detect yet")
    # else:
    #     return {"gas_quantity": last_rec["gas_quantity"], "status": last_rec["status"]}
# @router.get("/last")
# def last_quantity_status():
#     last_rec = mongo_connection["Record"].find().sort("datetime", -1).limit(1)
#     if not last_rec:
#         raise HTTPException(status_code=400, detail="Not detect yet")
#     else:
#         last_rec = last_rec[0]
#         return {"gas_quantity": last_rec["gas_quantity"], "status": last_rec["status"],
#                 "datetime": last_rec["datetime"]}
# @router.get("/last")
# def last_quantity_status():
#     records = list(mongo_connection["Record"].find())
#     if not records:
#         raise HTTPException(status_code=400, detail="Not detect yet")
#     else:
#         latest_datetime = records[0]["datetime"]
#         latest_record = records[0]
#         for record in records:
#             if record["datetime"] > latest_datetime:
#                 latest_datetime = record["datetime"]
#                 latest_record = record
#         return {"gas_quantity": latest_record["gas_quantity"], "status": latest_record["status"],
#                 "datetime": latest_record["datetime"]}


@router.get("/command")
def get_command():
    rec = mongo_connection["Record"].find_one({"isCommand": True})
    if not rec:
        raise HTTPException(status_code=400, detail="Not detect yet")
    else:
        return {"isOpen": rec["isOpen"]}
