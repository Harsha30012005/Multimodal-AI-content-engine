from pydantic import BaseModel
from typing import List

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

class CampaignResult(BaseModel):
    blog_post: BlogPost
    social_media: SocialMedia
    seo_metadata: SEOMetadata

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: dict = None