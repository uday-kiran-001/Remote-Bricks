from fastapi import FastAPI
from dotenv import load_dotenv
from pymongo import MongoClient
from routes import router as user_router
import os

load_dotenv()

ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")

app = FastAPI()

@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to the MongoDB database!")

@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()
    print("Closed connection to the MongoDB database!")

app.include_router(user_router, tags=["users"], prefix="/user")
