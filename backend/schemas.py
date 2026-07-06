from pydantic import BaseModel, field_validator
from typing import List, Optional

class CampaignRequest(BaseModel):
    campaign_brief: str
    tone: str = "professional"
    target_audience: str = "general"

    @field_validator('campaign_brief')
    def brief_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('campaign_brief cannot be empty')
        return v.strip()

    @field_validator('tone')
    def tone_must_be_valid(cls, v):
        allowed = ["professional", "casual", "formal", "friendly", "humorous"]
        if v.lower() not in allowed:
            return "professional"
        return v.lower()

class BlogPost(BaseModel):
    title: str = "Untitled Campaign"
    content_markdown: str = "Content not available"

class SocialMedia(BaseModel):
    twitter_variants: List[str] = ["Tweet 1", "Tweet 2", "Tweet 3"]

    @field_validator('twitter_variants')
    def must_have_three_tweets(cls, v):
        while len(v) < 3:
            v.append(f"Check out our latest campaign!")
        return v[:3]

class SEOMetadata(BaseModel):
    meta_title: str = "Campaign"
    meta_description: str = "Campaign description"
    keywords: List[str] = ["marketing", "campaign"]

class ImageAsset(BaseModel):
    url: str
    alt_description: str = "Campaign image"
    photographer: str = "Unknown"

class CampaignResult(BaseModel):
    blog_post: BlogPost
    social_media: SocialMedia
    seo_metadata: SEOMetadata
    images: List[ImageAsset] = []

class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[dict] = None