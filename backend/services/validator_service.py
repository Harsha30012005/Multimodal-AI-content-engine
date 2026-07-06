import json
import re
import logging
from schemas import BlogPost, SocialMedia, SEOMetadata, ImageAsset, CampaignResult

logger = logging.getLogger(__name__)

def clean_json_string(raw: str) -> str:
    # Remove markdown code blocks
    raw = raw.replace("```json", "").replace("```", "").strip()
    # Remove any leading/trailing whitespace
    raw = raw.strip()
    return raw

def validate_and_clean_result(raw_result: dict) -> dict:
    logger.info("Validating and cleaning result schema...")
    
    try:
        # Validate blog post
        blog_data = raw_result.get("blog_post", {})
        blog = BlogPost(
            title=blog_data.get("title", "Untitled Campaign"),
            content_markdown=blog_data.get("content_markdown", "Content not available")
        )

        # Validate social media
        social_data = raw_result.get("social_media", {})
        social = SocialMedia(
            twitter_variants=social_data.get("twitter_variants", [])
        )

        # Validate SEO metadata
        seo_data = raw_result.get("seo_metadata", {})
        seo = SEOMetadata(
            meta_title=seo_data.get("meta_title", "Campaign"),
            meta_description=seo_data.get("meta_description", "Campaign description"),
            keywords=seo_data.get("keywords", ["marketing"])
        )

        # Validate images
        images_data = raw_result.get("images", [])
        images = []
        for img in images_data:
            images.append(ImageAsset(
                url=img.get("url", ""),
                alt_description=img.get("alt_description", "Campaign image"),
                photographer=img.get("photographer", "Unknown")
            ))

        validated = CampaignResult(
            blog_post=blog,
            social_media=social,
            seo_metadata=seo,
            images=images
        )

        logger.info("Schema validation passed! ✅")
        return validated.model_dump()

    except Exception as e:
        logger.error(f"Schema validation failed: {str(e)}")
        raise ValueError(f"Schema validation error: {str(e)}")