from fastapi import FastAPI
from pydantic import BaseModel
from routers import add_data, get_record, update_command
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
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


# mock data
mock_data = [
    {
        "gas_quantity": 5,
        "time": datetime(2023, 2, 9, 11, 0, 0, 0),
        "status": "SAFE",
        "isCommand": False
    },
    {
        "gas_quantity": 10,
        "time": datetime(2023, 2, 9, 11, 5, 0, 0),
        "status": "SAFE",
        "isCommand": False
    },
    {
        "gas_quantity": 10,
        "time": datetime(2023, 2, 9, 11, 10, 0, 0),
        "status": "SAFE",
        "isCommand": False
    },
    {
        "gas_quantity": 60,
        "time": datetime(2023, 2, 9, 11, 15, 0, 0),
        "status": "WARNING",
        "isCommand": False
    },
    {
        "gas_quantity": 20,
        "time": datetime(2023, 2, 10, 10, 0, 0, 0),
        "status": "SAFE",
        "isCommand": False
    },
    {
        "gas_quantity": 80,
        "time": datetime(2023, 2, 10, 11, 0, 0, 0),
        "status": "DANGER",
        "isCommand": False
    },
]


# add mock data
@app.post("/addmock")
def add_mockdata():
    mongo_connection["Record"].insert_many(mock_data)


# delete all data except isCommand
@app.delete("/")
def delete_record():
    mongo_connection["Record"].delete_many({"isCommand": False})
