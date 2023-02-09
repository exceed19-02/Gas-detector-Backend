from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
from routers import add_data, get_record, update_command
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, Union
from datetime import date, datetime, timedelta
from database import mongo_connection

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# file based routing
app.include_router(get_record.router)
app.include_router(add_data.router)
app.include_router(update_command.router)


class Sensor(BaseModel):
    gas_quantity: Optional[int]
    time: Optional[datetime]
    status: Optional[str]
    isCommand: bool
    isOpen: Optional[bool]
