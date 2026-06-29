from celery_worker import celery_app
from services.ai_service import generate_campaign_content
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def generate_campaign_task(self, campaign_brief: str, tone: str = "professional", target_audience: str = "general"):
    try:
        logger.info(f"Starting task for: {campaign_brief}")
        result = generate_campaign_content(campaign_brief, tone, target_audience)
        logger.info("Task completed successfully!")
        return result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise self.retry(exc=e, countdown=3, max_retries=2)