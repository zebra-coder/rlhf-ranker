import google.generativeai as genai
from dotenv import load_dotenv 
import os

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ Error: No API Key found. Check your .env file.")
else:
    print("--- Asking Google for Available Models ---")
    
    try:
        # CORRECT SYNTAX for google-generativeai (Stable)
        genai.configure(api_key=api_key)
        
        # We loop through available models
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ Found: {m.name}")

    except Exception as e:
        print(f"Error: {e}")