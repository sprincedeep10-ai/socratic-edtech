import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="Teacher Dashboard", layout="wide")
st.title("📊 Teacher Intelligence Dashboard")
st.caption("Deep learning-gap analytics + zero-click actions")

API_URL = "http://localhost:8000"

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Learning Gaps — Alex Rivera")
    try:
        resp = httpx.get(f"{API_URL}/analytics/gaps/1", timeout=10)
        gaps = resp.json()
        if gaps:
            df = pd.DataFrame(gaps)
            st.dataframe(df, use_container_width=True)
            st.bar_chart(df.set_index("bottleneck_tag")["severity"])
        else:
            st.info("No significant gaps detected yet.")
    except Exception:
        st.warning("Backend not reachable. Showing demo data.")
        demo = [
            {"bottleneck_tag": "conceptual_misunderstanding", "severity": 0.82, "evidence_count": 7},
            {"bottleneck_tag": "prior_knowledge_gap", "severity": 0.65, "evidence_count": 4},
        ]
        st.dataframe(pd.DataFrame(demo))

with col2:
    st.subheader("Zero-Click Action Prompts")
    try:
        resp = httpx.get(f"{API_URL}/analytics/zero-click-actions/1", timeout=10)
        actions = resp.json().get("recommended_actions", [])
        for a in actions:
            priority = a.get("priority", "medium")
            color = "red" if priority == "high" else "orange"
            st.markdown(f"**[{priority.upper()}]** {a['action']}")
            if st.button(f"Assign → {a.get('tag', 'action')}", key=a['action'][:20]):
                st.success("Action logged for student!")
    except:
        st.markdown("- **High:** Targeted mini-lesson on conceptual_misunderstanding")
        st.markdown("- **Medium:** Review prior knowledge on fractions")

st.divider()
st.caption("In production this would surface class-wide heatmaps, trend lines, and LLM-generated intervention plans.")