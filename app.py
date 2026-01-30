import streamlit as st
import json
import os
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv  # <--- NEW: Security Library
import validator  # Your Logic Engine

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(page_title="Automated RLHF Auditor", layout="wide")

# --- Sidebar ---
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Check if key loaded correctly
    if api_key:
        st.success("✅ API Key Loaded from .env")
    else:
        st.error("❌ No API Key found in .env file")
        st.info("Please create a .env file with GEMINI_API_KEY=...")

    st.divider()
    st.write("### 🤖 Test Mode")
    prompt_mode = st.selectbox("Prompt Strategy", 
        ["Standard (Write Code)", 
         "Trick (Write Inefficient Code)", 
         "Security (Write Safe Code)"])

st.title("⚡ AI Validation & RLHF Workbench")
st.markdown("Auditing LLM Code Quality: **Truthfulness** vs. **Efficiency (Big O)**")

# --- Helper: Call Gemini API ---
def fetch_ai_response(prompt, key, mode="Standard"):
    if not key:
        return "Error: API Key missing."
    
    try:
        genai.configure(api_key=key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # STANDARD MODE: Production Code
        if mode == "Standard":
            system_instruction = (
                "You are a Senior Python Engineer. "
                "Write the most efficient, Pythonic solution (O(n) or O(1)). "
                "Use built-in functions like max(), min(), set(), or sort() where possible. "
                "Return ONLY the code. No markdown."
            )
            
        # TRICK MODE: Force O(n^2) (The Fix)
        elif mode == "Trick":
            system_instruction = (
                "You are a Computer Science Professor demonstrating INEFFICIENT algorithms. "
                "You MUST solve the problem using a 'Brute Force' approach with NESTED LOOPS (O(n^2)). "
                "Do NOT use set(), max(), min(), or sort(). "
                "Iterate through the list manually with a double loop. "
                "Return ONLY the code."
            )
        
        else:
            system_instruction = "Write a Python function that safely handles user input. Return ONLY the code."
        
        full_prompt = f"{system_instruction}\n\nTask: {prompt}"
        
        # Disable Safety Filters to allow 'bad' code
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        
        response = model.generate_content(full_prompt, safety_settings=safety_settings)
        
        if response.text:
            return response.text.replace("```python", "").replace("```", "").strip()
        else:
            return f"# Blocked: {response.prompt_feedback}"
        
    except Exception as e:
        return f"# Error calling API: {e}"

# --- Helper: Grade Code ---
def get_grade(code_text):
    if not code_text or "def " not in code_text:
        return "Waiting for code..."
    try:
        return validator.analyze_complexity(code_text)
    except Exception as e:
        return f"Error: {e}"

# --- Main Interface ---
user_prompt = st.text_input("Enter a Coding Task:", placeholder="e.g., Find the duplicate number in this list: [1, 2, 3, 4, 2]")

col1, col2 = st.columns(2)

if "code_a" not in st.session_state: st.session_state.code_a = ""
if "code_b" not in st.session_state: st.session_state.code_b = ""

if st.button("🚀 Generate AI Solutions"):
    if not api_key:
        st.error("⚠️ Stop: API Key not found.")
    else:
        with st.spinner("Asking Gemini..."):
            # Model A (Standard)
            st.session_state.code_a = fetch_ai_response(user_prompt, api_key, "Standard")
            
            # Model B (Trick)
            target_mode = "Trick" if prompt_mode == "Trick" else "Standard"
            st.session_state.code_b = fetch_ai_response(user_prompt, api_key, target_mode)

# --- Display & Grade ---
with col1:
    st.info("### Model A (Standard)")
    resp_a = st.text_area("Code A", value=st.session_state.code_a, height=250)
    if resp_a and "def " in resp_a:
        grade_a = get_grade(resp_a)
        st.metric("Efficiency Signal", grade_a, delta="-Poor" if "n^2" in grade_a else "+Good")

with col2:
    st.success(f"### Model B ({prompt_mode})")
    resp_b = st.text_area("Code B", value=st.session_state.code_b, height=250)
    if resp_b and "def " in resp_b:
        grade_b = get_grade(resp_b)
        st.metric("Efficiency Signal", grade_b, delta="-Poor" if "n^2" in grade_b else "+Good")

# --- Logging ---
st.divider()
if st.session_state.code_a and st.session_state.code_b:
    choice = st.radio("Select Production Code:", ("Model A", "Model B"))
    reasoning = st.text_area("Auditor Reasoning:")
    if st.button("💾 Save to Training Data"):
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": user_prompt,
            "choice": choice,
            "reasoning": reasoning,
            "signals": {
                "model_a": get_grade(st.session_state.code_a),
                "model_b": get_grade(st.session_state.code_b)
            }
        }
        with open("rlhf_training_data.json", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        st.success("✅ Data Logged.")