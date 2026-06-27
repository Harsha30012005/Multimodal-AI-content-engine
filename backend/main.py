from fastapi import FastAPI
from routes.campaign import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="MultiModal AI Content Engine")

app.include_router(router)

@app.get("/")
def root():
    redis_url = os.getenv("REDIS_URL")
    return {
        "message": "MultiModal AI Content Engine is running!",
        "redis_url": redis_url
    }