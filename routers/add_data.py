from fastapi import APIRouter, Body, HTTPException
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from database import mongo_connection

router = APIRouter(
    prefix="/add",
    tags=["add"],
    responses={404: {"description": "Not found"}},
)


class Sensor(BaseModel):
    gas_quantity: Optional[int]
    time: Optional[datetime]
    status: Optional[str]
    isCommand: bool
    isOpen: Optional[bool]


# add new record by input gas_quantity and status in body format
@router.post("/", status_code=201)
def add_record(gas_quantity: int = Body(), status: str = Body()):
    if gas_quantity < 0 or gas_quantity > 4095:
        raise HTTPException(status_code=400, detail="Gas Quantity out of range")
    data = {
        "gas_quantity": gas_quantity,
        "time": datetime.now(),
        "status": status,
        "isCommand": False
    }
    mongo_connection["Record"].insert_one(data)
    return {"message": "Record created"}
