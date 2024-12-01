from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as trade_router
from contextlib import asynccontextmanager

config = dotenv_values(".env")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize MongoDB client
    app.mongodb_client = MongoClient(config["MONGO_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("MongoDB client connected.")

    yield  # Application runs here

    # Shutdown: Close MongoDB client
    app.mongodb_client.close()
    print("MongoDB client closed.")

# Initialize FastAPI with the lifespan context manager
app = FastAPI(lifespan=lifespan)

# Include router
app.include_router(trade_router, tags=["trade-events"], prefix="/trade")
