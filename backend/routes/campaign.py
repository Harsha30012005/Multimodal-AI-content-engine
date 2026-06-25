from fastapi import APIRouter

router = APIRouter()

@router.post("/generate")
def generate_campaign(campaign_brief: str):
    return {"message": "Campaign generation will be implemented here"}

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    return {"task_id": task_id, "status": "pending"}