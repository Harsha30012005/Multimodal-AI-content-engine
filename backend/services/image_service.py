import requests
import os
from dotenv import load_dotenv
import logging

basedir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(basedir, '..', '.env')
load_dotenv(env_path)

logger = logging.getLogger(__name__)
UNSPLASH_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

def generate_campaign_images(campaign_brief: str, count: int = 2) -> list:
    logger.info(f"Fetching images for: {campaign_brief}")
    
    try:
        url = "https://api.unsplash.com/search/photos"
        params = {
            "query": campaign_brief,
            "per_page": count,
            "client_id": UNSPLASH_KEY
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        images = []
        for photo in data.get("results", [])[:count]:
            images.append({
                "url": photo["urls"]["regular"],
                "alt_description": photo.get("alt_description", campaign_brief),
                "photographer": photo["user"]["name"]
            })

        if not images:
            return get_fallback_images(campaign_brief, count)

        logger.info(f"Fetched {len(images)} images successfully!")
        return images

    except Exception as e:
        logger.warning(f"Image API unavailable: {str(e)}. Using fallback images.")
        return get_fallback_images(campaign_brief, count)


def get_fallback_images(campaign_brief: str, count: int = 2) -> list:
    return [
        {
            "url": f"https://placehold.co/800x600?text={campaign_brief.replace(' ', '+')}",
            "alt_description": f"Placeholder image for {campaign_brief}",
            "photographer": "Placeholder"
        }
        for _ in range(count)
    ]