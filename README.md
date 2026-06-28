# Multi-Modal AI Content Marketing Engine
## Member 2 — Backend Architecture & Task Queue Operations

### Project Overview
A production-grade async backend API that powers the Multi-Modal AI Content 
Marketing Engine. Accepts campaign briefs and processes them through a 
distributed task queue to generate marketing content.

### My Responsibilities
- REST API setup using FastAPI
- Redis + Celery async task queue
- POST /generate and GET /tasks/{id} endpoints
- Error handling and logging
- Pydantic schema validation

### Tech Stack
- Python 3.x
- FastAPI
- Celery 5.3.4
- Redis
- Pydantic
- Uvicorn

### Project Structure
multimodal-ai-content-engine/
│
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── celery_worker.py     # Celery configuration
│   ├── tasks.py             # Background task definitions
│   ├── schemas.py           # Pydantic request/response models
│   ├── routes/
│   │   └── campaign.py      # API route handlers
│   └── .env                 # Environment variables (gitignored)
│
├── requirements.txt
├── .gitignore
└── README.md

### API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | / | Root health check |
| GET | /health | Service health status |
| POST | /generate | Submit campaign brief |
| GET | /tasks/{task_id} | Check task status |

### How to Run Locally

#### 1. Clone the repo
git clone https://github.com/Harsha30012005/Multimodal-AI-content-engine.git
cd Multimodal-AI-content-engine

#### 2. Create virtual environment
python -m venv venv
venv\Scripts\activate

#### 3. Install dependencies
pip install -r requirements.txt

#### 4. Start Redis
Make sure Redis is running as Windows service

#### 5. Start Celery Worker (Terminal 1)
cd backend
celery -A celery_worker worker --loglevel=info -P solo

#### 6. Start FastAPI (Terminal 2)
cd backend
uvicorn main:app --reload

#### 7. Test API
Visit http://127.0.0.1:8000/docs

### Sample Request
POST /generate
{
  "campaign_brief": "eco-friendly sneakers",
  "tone": "casual",
  "target_audience": "young adults"
}

### Sample Response
GET /tasks/{task_id}
{
  "task_id": "abc123",
  "status": "completed",
  "result": {
    "blog_post": {
      "title": "Campaign for eco-friendly sneakers",
      "content_markdown": "..."
    },
    "social_media": {
      "twitter_variants": ["Tweet 1", "Tweet 2", "Tweet 3"]
    },
    "seo_metadata": {
      "meta_title": "Best eco-friendly sneakers",
      "meta_description": "...",
      "keywords": ["eco-friendly", "sneakers"]
    }
  }
}