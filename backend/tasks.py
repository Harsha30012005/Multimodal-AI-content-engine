from celery_worker import celery_app
import time

@celery_app.task(bind=True)
def generate_campaign_task(self, campaign_brief):
    try:
        time.sleep(5)
        return {
            "status": "completed",
            "campaign_brief": campaign_brief,
            "result": {
                "blog_post": {
                    "title": f"Campaign for {campaign_brief}",
                    "content_markdown": "This is a sample blog post content."
                },
                "social_media": {
                    "twitter_variants": [
                        f"Tweet 1 about {campaign_brief}",
                        f"Tweet 2 about {campaign_brief}",
                        f"Tweet 3 about {campaign_brief}"
                    ]
                },
                "seo_metadata": {
                    "meta_title": f"Best {campaign_brief}",
                    "meta_description": f"Discover our amazing {campaign_brief}",
                    "keywords": [campaign_brief, "marketing", "campaign"]
                }
            }
        }
    except Exception as e:
        raise self.retry(exc=e, countdown=3, max_retries=2)