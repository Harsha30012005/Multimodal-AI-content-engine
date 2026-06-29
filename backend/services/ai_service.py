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
print(f"API KEY LOADED: {api_key[:15] if api_key else 'NOT FOUND'}")

logger = logging.getLogger(__name__)
client = anthropic.Anthropic(api_key=api_key)