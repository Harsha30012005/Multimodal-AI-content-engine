from fastapi import FastAPI
from dotenv import load_dotenv
import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

from routes.campaign import router

app = FastAPI(
    title="MultiModal AI Content Engine",
    description="Member 2 - Backend Architecture & Task Queue",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {
        "message": "MultiModal AI Content Engine is running!",
        "redis_url": os.getenv("REDIS_URL"),
        "version": "1.0.0"
    }

@app.get("/health")
def health_check():
    logger.info("Health check called")
    return {
        "status": "healthy",
        "redis": "connected",
        "celery": "running"
    }