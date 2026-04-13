import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv("bot_token")
groq_api_key = os.getenv("GROQ_API_KEY")

if not bot_token or not groq_api_key:
    raise ValueError("API tokens are not set in .env file")