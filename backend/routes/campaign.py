from fastapi import APIRouter
from schemas import CampaignRequest, TaskResponse
from tasks import generate_campaign_task

router = APIRouter()

@router.post("/generate", response_model=TaskResponse)
def generate_campaign(request: CampaignRequest):
    task = generate_campaign_task.delay(
        request.campaign_brief,
        request.tone,
        request.target_audience
    )
    return {
        "task_id": task.id,
        "status": "processing",
        "result": None
    }

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_status(task_id: str):
    task = generate_campaign_task.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"task_id": task_id, "status": "pending", "result": None}
    elif task.state == "SUCCESS":
        return {"task_id": task_id, "status": "completed", "result": task.result}
    elif task.state == "FAILURE":
        return {"task_id": task_id, "status": "failed", "result": None}
    else:
        return {"task_id": task_id, "status": "processing", "result": None}