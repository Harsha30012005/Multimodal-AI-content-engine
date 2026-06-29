from openai import OpenAI
import os
import json
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional marketing copywriter. Always respond with valid JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=1500
    )
    
    content = response.choices[0].message.content
    
    # Clean any markdown code blocks if present
    content = content.replace("```json", "").replace("```", "").strip()
    
    result = json.loads(content)
    logger.info("Content generated successfully!")
    
    return result