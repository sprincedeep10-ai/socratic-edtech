import streamlit as st
import httpx

st.set_page_config(page_title="Parent Companion", page_icon="👨‍👩‍👧")
st.title("👨‍👩‍👧 Parent Companion")
st.caption("Clear, jargon-free insights + simple micro-actions")

API_URL = "http://localhost:8000"

try:
    resp = httpx.get(f"{API_URL}/parent/summary/1", timeout=10)
    data = resp.json()
except Exception:
    data = {
        "summary_text": "Your child is showing signs of difficulty connecting ideas in math. They understand the steps but struggle with the 'why'.",
        "micro_actions": [
            "Ask them to explain one problem in their own words tonight.",
            "Try the 'teach me like I'm 5' game on the current topic."
        ]
    }

st.markdown("### This Week's Insight")
st.info(data["summary_text"])

st.markdown("### Simple Things You Can Do")
for action in data.get("micro_actions", []):
    st.checkbox(action, key=action)

st.divider()
st.caption("Powered by SocraticEd • No education jargon. Just clear next steps.")