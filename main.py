from fastapi import FastAPI
from contextlib import asynccontextmanager
from pymongo import MongoClient
from routes import router as user_router
from dotenv import load_dotenv
import os

load_dotenv()

ATLAS_URI = os.getenv("ATLAS_URI")
DB_NAME = os.getenv("DB_NAME")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Connect to the MongoDB database
    app.mongodb_client = MongoClient(ATLAS_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to the MongoDB database!")
    yield
    # Shutdown: Close the MongoDB connection
    app.mongodb_client.close()
    print("Closed connection to the MongoDB database!")

app = FastAPI(lifespan=lifespan)

app.include_router(user_router, tags=["users"], prefix="/user")
