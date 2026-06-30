from celery_worker import celery_app
import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import generate_campaign_content
from services.image_service import generate_campaign_images

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def generate_campaign_task(self, campaign_brief: str, tone: str = "professional", target_audience: str = "general"):
    try:
        logger.info(f"Starting task for: {campaign_brief}")
        
        text_result = generate_campaign_content(campaign_brief, tone, target_audience)
        images_result = generate_campaign_images(campaign_brief, count=2)
        
        text_result["images"] = images_result
        
        logger.info("Task completed successfully!")
        return text_result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise self.retry(exc=e, countdown=3, max_retries=2)