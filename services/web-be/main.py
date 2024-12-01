from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
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

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=[

        "http://localhost:3000",  # React frontend
        "http://127.0.0.1:3000",  # Another way localhost might be accessed
    ],  # Allow specific origins
    allow_credentials=True,  # Allow cookies to be sent with requests
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include router
app.include_router(trade_router, tags=["trade-events"], prefix="/trade")
