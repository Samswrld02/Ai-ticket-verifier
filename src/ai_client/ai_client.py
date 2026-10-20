from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

aiclient = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)