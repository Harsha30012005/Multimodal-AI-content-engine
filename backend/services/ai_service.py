import anthropic
import os
import json
from dotenv import load_dotenv
import logging

# Load .env from backend folder directly
basedir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(basedir, '..', '.env')
load_dotenv(env_path)

api_key = os.getenv("ANTHROPIC_API_KEY")
logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=api_key)

def generate_campaign_content(campaign_brief: str, tone: str, target_audience: str) -> dict:
    logger.info(f"Generating content for: {campaign_brief}")
    
    prompt = f"""
    You are a professional digital marketing copywriter.
    
    Generate marketing content for the following campaign:
    - Campaign Brief: {campaign_brief}
    - Tone: {tone}
    - Target Audience: {target_audience}
    
    Return ONLY a valid JSON object with this exact structure, no extra text:
    {{
        "blog_post": {{
            "title": "engaging blog title here",
            "content_markdown": "full blog post content in markdown here"
        }},
        "social_media": {{
            "twitter_variants": [
                "tweet 1 under 280 chars",
                "tweet 2 under 280 chars",
                "tweet 3 under 280 chars"
            ]
        }},
        "seo_metadata": {{
            "meta_title": "SEO optimized title",
            "meta_description": "SEO meta description under 160 chars",
            "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"]
        }}
    }}
    """
    
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
    logger.info("Content generated successfully!")
    
    return result