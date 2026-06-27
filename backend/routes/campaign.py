from fastapi import APIRouter
from tasks import generate_campaign_task

router = APIRouter()

@router.post("/generate")
def generate_campaign(campaign_brief: str):
    task = generate_campaign_task.delay(campaign_brief)
    return {
        "message": "Campaign generation started!",
        "task_id": task.id,
        "status": "processing"
    }

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = generate_campaign_task.AsyncResult(task_id)
    
    if task.state == "PENDING":
        return {"task_id": task_id, "status": "pending"}
    elif task.state == "SUCCESS":
        return {"task_id": task_id, "status": "completed", "result": task.result}
    elif task.state == "FAILURE":
        return {"task_id": task_id, "status": "failed"}
    else:
        return {"task_id": task_id, "status": "processing"}