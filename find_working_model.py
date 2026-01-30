import google.generativeai as genai
from dotenv import load_dotenv 
import os

# --- PASTE YOUR REAL KEY HERE ---
# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

print("--- Hunting for a working model ---")

# The most likely active models in 2026
candidates = [
    "gemini-2.0-flash",       # The standard workhorse
    "gemini-2.0-flash-001",   # The specific version
    "gemini-2.5-flash",       # The upgraded version
    "gemini-1.5-flash-latest" # The legacy fallback
]

found = False
for model_name in candidates:
    print(f"Testing: {model_name}...", end=" ")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Say 'Hello'")
        print("✅ SUCCESS!")
        print(f"\n>>> UPDATE YOUR APP.PY TO USE: '{model_name}'")
        found = True
        break
    except Exception as e:
        print("❌")

if not found:
    print("\n⚠️ ALL FAILED. Check your API Key characters carefully.")