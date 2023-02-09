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

@router.get("/")
def root():
    return {"msg": "Hello World"}