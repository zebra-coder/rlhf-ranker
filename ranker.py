import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="RLHF Preference Ranker", layout="wide")

st.title("AI Response Evaluation Portal")
st.subheader("Goal: Rank responses based on truthfulness and reasoning.")

col1, col2 = st.columns(2)

with col1:
    st.info("### Response A")
    resp_a = st.text_area("Content A", "The capital of France is Paris.", height=150, disabled=True)

with col2:
    st.success("### Response B")
    resp_b = st.text_area("Content B", "Paris is the capital and largest city of France.", height=150, disabled=True)

# Ranking Logic
choice = st.radio("Which response is superior?", ("Response A", "Response B", "Tie"))
reasoning = st.text_area("Provide a step-by-step reasoning for your choice:")

if st.button("Submit Rank"):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "choice": choice,
        "reasoning": reasoning,
        "metadata": {"model_a_len": len(resp_a), "model_b_len": len(resp_b)}
    }
    
    # Save to local JSON (Synthetic Data Pipeline)
    with open("rlhf_log.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")
    
    st.balloons()
    st.success("Data logged for model fine-tuning.")