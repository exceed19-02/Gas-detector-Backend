import os
from pymongo import MongoClient
from dotenv import load_dotenv

# import env
load_dotenv(".env")
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
# connect database
client = MongoClient(
    f"mongodb://{username}:{password}@mongo.exceed19.online:8443/?authMechanism=DEFAULT"
)
# select database
mongo_connection = client["exceed02"]  # use exceed02
