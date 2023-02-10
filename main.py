from fastapi import FastAPI
from pydantic import BaseModel
from routers import add_data, get_record, update_command
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from datetime import datetime
from database import mongo_connection
from random import randint

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
mock_data = []
for i in range(-1,23,-1):
    mock_data.append({
        "gas_quantity": randint(10,2000),
        "time": datetime.fromtimestamp(datetime.now().timestamp()-(2500+(i*3600))),
        "status": "DANGER",
        "isCommand": False
    })
    mock_data.append({
        "gas_quantity": randint(10,2000),
        "time": datetime.fromtimestamp(datetime.now().timestamp()-(1300+(i*3600))),
        "status": "DANGER",
        "isCommand": False
    })
    mock_data.append({
        "gas_quantity": randint(10,2000),
        "time": datetime.fromtimestamp(datetime.now().timestamp()-(100+(i*3600))),
        "status": "DANGER",
        "isCommand": False
    })


# add mock data
@app.post("/addmock")
def add_mockdata():
    mongo_connection["Record"].insert_many(mock_data)


# delete all data except isCommand
@app.delete("/")
def delete_record():
    mongo_connection["Record"].delete_many({"isCommand": False})
