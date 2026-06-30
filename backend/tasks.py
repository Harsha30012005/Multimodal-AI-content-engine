from celery_worker import celery_app
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.ai_service import generate_campaign_content
from services.image_service import generate_campaign_images

logger = logging.getLogger(__name__)

@celery_app.task(bind=True)
def generate_campaign_task(self, campaign_brief: str, tone: str = "professional", target_audience: str = "general"):
    try:
        logger.info(f"Starting PARALLEL task for: {campaign_brief}")
        start_time = time.time()

        with ThreadPoolExecutor(max_workers=2) as executor:
            text_future = executor.submit(generate_campaign_content, campaign_brief, tone, target_audience)
            image_future = executor.submit(generate_campaign_images, campaign_brief, 2)

            text_result = text_future.result()
            images_result = image_future.result()

        text_result["images"] = images_result

        elapsed = round(time.time() - start_time, 2)
        logger.info(f"Task completed in {elapsed}s using parallel execution!")

        text_result["_meta"] = {"execution_time_seconds": elapsed, "mode": "parallel"}

        return text_result
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        raise self.retry(exc=e, countdown=3, max_retries=2)