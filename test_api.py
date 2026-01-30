import google.generativeai as genai
from dotenv import load_dotenv 
import os

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

print("--- Starting Connection Test ---")

if not api_key:
    print("❌ Error: Could not find 'GEMINI_API_KEY' in your .env file.")
else:
    try:
        # CORRECT SYNTAX (Stable Library)
        # We don't use 'Client', we use 'configure'
        genai.configure(api_key=api_key)
        
        # 2. Define the Model
        print("Attempting to contact Gemini...")
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # 3. Generate
        response = model.generate_content('Write a Python print statement that says "Hello World".')
        
        # 4. Success
        print("\n✅ SUCCESS! Reply received:")
        print(response.text)

    except Exception as e:
        print("\n❌ FAILED.")
        print(f"Error Details: {e}")