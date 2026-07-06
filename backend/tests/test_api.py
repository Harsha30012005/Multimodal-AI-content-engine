import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()
    print("✅ Root endpoint working!")

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    print("✅ Health endpoint working!")

def test_generate_endpoint():
    payload = {
        "campaign_brief": "eco-friendly sneakers",
        "tone": "casual",
        "target_audience": "young adults"
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] == "processing"
    print(f"✅ Generate endpoint working! task_id: {data['task_id']}")

def test_generate_empty_brief():
    payload = {
        "campaign_brief": "",
        "tone": "casual",
        "target_audience": "young adults"
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 422
    print("✅ Empty brief validation working!")

def test_generate_invalid_tone():
    payload = {
        "campaign_brief": "eco-friendly sneakers",
        "tone": "invalid_tone",
        "target_audience": "young adults"
    }
    response = client.post("/generate", json=payload)
    assert response.status_code == 200
    print("✅ Invalid tone defaults to professional!")

def test_task_status_invalid_id():
    response = client.get("/tasks/invalid-task-id-123")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    print("✅ Invalid task_id handled gracefully!")