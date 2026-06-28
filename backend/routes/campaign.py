from fastapi import APIRouter, HTTPException
from schemas import CampaignRequest, TaskResponse
from tasks import generate_campaign_task
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/generate")
def generate_campaign(request: CampaignRequest):
    try:
        logger.info(f"Received campaign request: {request.campaign_brief}")
        task = generate_campaign_task.delay(
            request.campaign_brief,
            request.tone,
            request.target_audience
        )
        logger.info(f"Task created with ID: {task.id}")
        return {
            "task_id": task.id,
            "status": "processing",
            "result": None
        }
    except Exception as e:
        logger.error(f"Error creating task: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    try:
        logger.info(f"Checking status for task: {task_id}")
        task = generate_campaign_task.AsyncResult(task_id)

        if task.state == "PENDING":
            return {"task_id": task_id, "status": "pending", "result": None}
        elif task.state == "SUCCESS":
            logger.info(f"Task {task_id} completed successfully")
            return {"task_id": task_id, "status": "completed", "result": task.result}
        elif task.state == "FAILURE":
            logger.error(f"Task {task_id} failed")
            return {"task_id": task_id, "status": "failed", "result": None}
        else:
            return {"task_id": task_id, "status": "processing", "result": None}
    except Exception as e:
        logger.error(f"Error checking task status: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))