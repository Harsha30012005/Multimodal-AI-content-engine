from pydantic import BaseModel
from typing import List, Optional

class CampaignRequest(BaseModel):
    campaign_brief: str
    tone: str = "professional"
    target_audience: str = "general"

class BlogPost(BaseModel):
    title: str
    content_markdown: str

class SocialMedia(BaseModel):
    twitter_variants: List[str]

class SEOMetadata(BaseModel):
    meta_title: str
    meta_description: str
    keywords: List[str]

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[dict] = None