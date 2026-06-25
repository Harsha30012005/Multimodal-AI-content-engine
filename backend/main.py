from fastapi import FastAPI
from routes.campaign import router

app = FastAPI(title="MultiModal AI Content Engine")

app.include_router(router)

@app.get("/")
def root():
    return {"message": "MultiModal AI Content Engine is running!"}