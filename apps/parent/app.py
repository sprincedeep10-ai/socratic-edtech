import streamlit as st
import httpx

st.set_page_config(page_title="Parent Companion", page_icon="👨‍👩‍👧")
st.title("👨‍👩‍👧 Parent Companion — 家長伴侶")
st.caption("Clear, jargon-free insights + simple micro-actions (English + 粵語)")

DEFAULT_DEPLOYED = "https://socratic-edtech.onrender.com"
DEFAULT_LOCAL = "http://localhost:8000"

with st.sidebar:
    env = st.selectbox("Backend", ["Deployed (Render)", "Local"], index=0)
    API_URL = DEFAULT_DEPLOYED if "Deployed" in env else DEFAULT_LOCAL
    st.caption(f"Using: {API_URL}")
    if st.button("Refresh"):
        st.rerun()

student_id = 1

try:
    resp = httpx.get(f"{API_URL}/parent/summary/{student_id}", timeout=30)
    data = resp.json()
except Exception as e:
    st.warning(f"Using demo (backend issue: {e})")
    data = {
        "summary_text": "Your child is showing signs of difficulty connecting ideas in math. They understand the steps but struggle with the 'why'.",
        "micro_actions": [
            "[EN] Tonight ask Alex to explain why multiplying top and bottom by the same number keeps the fraction the same. Use paper cutting to show.",
            "[粵語] 今晚問阿豪點解分子同分母乘同一數，分數值唔變。用紙剪一剪俾佢睇。"
        ],
        "generated_at": "2026-08-16"
    }

st.markdown("### This Week's Insight / 本週洞察")
st.info(data.get("summary_text", "Progressing well."))

st.markdown("### Simple Things You Can Do / 你可以做嘅簡單事")
actions = data.get("micro_actions", [])
for i, action in enumerate(actions):
    checked = st.checkbox(action, key=f"action_{i}")
    if checked:
        st.success("Great — small consistent actions make a big difference! / 好！細微持續嘅行動好重要！")

st.divider()
st.caption("Powered by SocraticEd • No education jargon. Just clear next steps. • 全雙語支援 (English / 粵語)")
st.caption(f"Last generated: {data.get('generated_at', '')}")
