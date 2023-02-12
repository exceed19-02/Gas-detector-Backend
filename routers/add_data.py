from datetime import datetime
from typing import Optional, Dict, Union

from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel

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


@router.post("", status_code=201)
def add_record(gas_quantity: int = Body(), status: str = Body()):
    """add new record by input gas_quantity and status in body format

    Keyword Arguments:
        gas_quantity {int} -- _description_ (default: {Body()})
        status {str} -- _description_ (default: {Body()})

    Raises:
        HTTPException: _description_

    Returns:
        _type_ -- _description_
    """
    if gas_quantity < 0 or gas_quantity > 4095:
        raise HTTPException(status_code=400, detail="Gas Quantity out of range")
    data = {
        "gas_quantity": gas_quantity,
        "time": datetime.now(),
        "status": status,
        "isCommand": False,
    }
    mongo_connection["Record"].insert_one(data)
    return {"message": "Record created"}
