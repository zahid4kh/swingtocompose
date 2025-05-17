from dotenv import load_dotenv
import google.generativeai as genai
import os


load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Warning: GEMINI_API_KEY not found in .env file")  # demo

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
