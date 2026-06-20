from dotenv import load_dotenv
import os
from google import genai

# Load all Environemnt Variables(.env File)
load_dotenv()

# Setup Gemini API Key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("❌ GEMINI_API_KEY is missing! Please check your .env file or environment variables.")

client = genai.Client()
DB_PATH = "Faculty.db"

