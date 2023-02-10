from fastapi import APIRouter, Body
from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from utils import get_bangkok_time
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

    data = {
        "gas_quantity": gas_quantity,
        "time":get_bangkok_time(),
        "status": status,
        "isCommand": False
    }
    mongo_connection["Record"].insert_one(data)
    return {"message": "Record created"}
