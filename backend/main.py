from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

from routes.campaign import router

app = FastAPI(title="MultiModal AI Content Engine")

app.include_router(router)

@app.get("/")
def root():
    return {
        "message": "MultiModal AI Content Engine is running!",
        "redis_url": os.getenv("REDIS_URL")
    }