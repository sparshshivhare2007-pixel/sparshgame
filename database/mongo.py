# database/mongo.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# COMMON COLLECTIONS
users = db["users"]
groups = db["groups"]
chatbot_collection = db["chatbot"]
