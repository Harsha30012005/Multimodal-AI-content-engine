import anthropic
import os
import json
from dotenv import load_dotenv
import logging

basedir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(basedir, '..', '.env')
load_dotenv(env_path)

api_key = os.getenv("ANTHROPIC_API_KEY")
logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=api_key)

def get_fallback_content(campaign_brief: str, tone: str, target_audience: str) -> dict:
    logger.info("Using fallback content generator")
    return {
        "blog_post": {
            "title": f"Introducing {campaign_brief} — A Game Changer for {target_audience}",
            "content_markdown": f"## Why {campaign_brief} is Perfect for {target_audience}\n\nIn today's world, {campaign_brief} represents a new era of innovation. With a {tone} approach, we bring you the best experience tailored specifically for {target_audience}.\n\n### Key Benefits\n- Premium quality\n- Sustainable choice\n- Perfect for {target_audience}\n\n### Conclusion\nDon't miss out on {campaign_brief}. Join thousands of satisfied customers today!"
        },
        "social_media": {
            "twitter_variants": [
                f"🌟 Introducing {campaign_brief}! Perfect for {target_audience}. Get yours today! #trending",
                f"Why {target_audience} love {campaign_brief} — discover the difference today! 🚀",
                f"The future is here! {campaign_brief} is everything {target_audience} have been waiting for! 💫"
            ]
        },
        "seo_metadata": {
            "meta_title": f"Best {campaign_brief} for {target_audience} | Shop Now",
            "meta_description": f"Discover {campaign_brief} — the perfect choice for {target_audience}. {tone.capitalize()} style, premium quality.",
            "keywords": [campaign_brief, target_audience, tone, "marketing", "campaign", "trending"]
        }
    }

def generate_campaign_content(campaign_brief: str, tone: str, target_audience: str) -> dict:
    logger.info(f"Generating content for: {campaign_brief}")
    
    prompt = f"""
    You are a professional digital marketing copywriter.
    Generate marketing content for:
    - Campaign Brief: {campaign_brief}
    - Tone: {tone}
    - Target Audience: {target_audience}
    
    Return ONLY valid JSON with this structure:
    {{
        "blog_post": {{
            "title": "engaging title",
            "content_markdown": "full blog post in markdown"
        }},
        "social_media": {{
            "twitter_variants": ["tweet1", "tweet2", "tweet3"]
        }},
        "seo_metadata": {{
            "meta_title": "SEO title",
            "meta_description": "SEO description under 160 chars",
            "keywords": ["keyword1", "keyword2", "keyword3"]
        }}
    }}
    """
    
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        content = response.content[0].text
        content = content.replace("```json", "").replace("```", "").strip()
        result = json.loads(content)
        logger.info("AI content generated successfully!")
        return result

    except Exception as e:
        logger.warning(f"AI API unavailable: {str(e)}. Using fallback content.")
        return get_fallback_content(campaign_brief, tone, target_audience)