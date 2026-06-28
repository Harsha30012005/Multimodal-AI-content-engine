from celery_worker import celery_app
import time

@celery_app.task(bind=True)
def generate_campaign_task(self, campaign_brief: str, tone: str = "professional", target_audience: str = "general"):
    try:
        time.sleep(5)
        return {
            "blog_post": {
                "title": f"Campaign for {campaign_brief}",
                "content_markdown": f"This is a {tone} blog post targeting {target_audience} about {campaign_brief}."
            },
            "social_media": {
                "twitter_variants": [
                    f"Tweet 1 ({tone}): Discover {campaign_brief}!",
                    f"Tweet 2 ({tone}): {campaign_brief} is perfect for {target_audience}!",
                    f"Tweet 3 ({tone}): Get yours now — {campaign_brief}!"
                ]
            },
            "seo_metadata": {
                "meta_title": f"Best {campaign_brief} for {target_audience}",
                "meta_description": f"Discover our amazing {campaign_brief}. Perfect for {target_audience}.",
                "keywords": [campaign_brief, tone, target_audience, "marketing", "campaign"]
            }
        }
    except Exception as e:
        raise self.retry(exc=e, countdown=3, max_retries=2)