from fastapi import APIRouter, Body
from typing import Union, Optional
from pydantic import BaseModel
from datetime import date, datetime
from database import mongo_connection

router = APIRouter(
    prefix="/update",
    tags=["update"],
    responses={404: {"description": "Not found"}},
)


@router.put("/", status_code=205)
def root():
    """
    upgrade status of isOpen table in database
    """
    is_open = mongo_connection["Record"].find_one(
        {"isCommand": True}, {"isCommand": False, '_id': False})["isOpen"]

    mongo_connection["Record"].update_one(
        {"isCommand": True}, {"$set": {"isOpen": not is_open}})
    return {"message": f"already update command to {not is_open}"}
