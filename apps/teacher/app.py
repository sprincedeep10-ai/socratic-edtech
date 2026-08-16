import streamlit as st
import httpx
import pandas as pd

st.set_page_config(page_title="Teacher Dashboard", layout="wide")
st.title("📊 Teacher Intelligence Dashboard — 教師智能儀表板")
st.caption("Deep learning-gap analytics + zero-click recommended actions (bilingual)")

# Config
DEFAULT_DEPLOYED = "https://socratic-edtech.onrender.com"
DEFAULT_LOCAL = "http://localhost:8000"

with st.sidebar:
    env = st.selectbox("Backend", ["Deployed (Render)", "Local"], index=0)
    API_URL = DEFAULT_DEPLOYED if "Deployed" in env else DEFAULT_LOCAL
    st.caption(f"Using: {API_URL}")
    if st.button("Refresh Data"):
        st.rerun()

student_id = 1  # Alex for now

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Learning Gaps — Alex Chan (陳偉豪)")
    try:
        resp = httpx.get(f"{API_URL}/analytics/gaps/{student_id}", timeout=30)
        gaps = resp.json()
        if gaps:
            # Normalize for display (handle nested tag)
            rows = []
            for g in gaps:
                tag = g.get("tag") or {}
                rows.append({
                    "tag_id": g.get("tag_id"),
                    "bottleneck_en": tag.get("name_en") or g.get("tag_id"),
                    "bottleneck_yue": tag.get("name_yue", ""),
                    "severity": round(g.get("severity", 0), 2),
                    "evidence_count": g.get("evidence_count", 1),
                    "context": g.get("context_notes", "")
                })
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)

            # Bar chart on severity
            if not df.empty:
                chart_df = df.set_index("bottleneck_en")["severity"]
                st.bar_chart(chart_df)
        else:
            st.info("No significant gaps detected yet.")
    except Exception as e:
        st.warning(f"Backend not reachable ({e}). Showing demo bilingual data.")
        demo = [
            {"tag_id": 1, "bottleneck_en": "Fraction Expansion Gaps", "bottleneck_yue": "分數擴展缺口", "severity": 0.82, "evidence_count": 7, "context": "Seen in chat and worksheet Q4-7"},
            {"tag_id": 3, "bottleneck_en": "Prior Knowledge Gap - Multiples", "bottleneck_yue": "倍數前備知識缺口", "severity": 0.65, "evidence_count": 4, "context": ""},
        ]
        df = pd.DataFrame(demo)
        st.dataframe(df, use_container_width=True)
        st.bar_chart(df.set_index("bottleneck_en")["severity"])

with col2:
    st.subheader("Zero-Click Action Prompts")
    try:
        resp = httpx.get(f"{API_URL}/analytics/zero-click-actions/{student_id}", timeout=30)
        actions = resp.json().get("recommended_actions", [])
        for a in actions:
            priority = a.get("priority", "medium")
            color = "🔴" if priority == "high" else "🟠"
            en = a.get("tag_en") or a.get("tag", "")
            yue = a.get("tag_yue", "")
            display = f"{en} ({yue})" if yue else en
            st.markdown(f"{color} **[{priority.upper()}]** {a.get('action', '')}")
            if st.button(f"Assign → {display[:30]}", key=str(a)[:30]):
                st.success("Action logged for student! (prototype)")
    except Exception as e:
        st.markdown("🔴 **High:** Targeted mini-lesson on Fraction Expansion Gaps (分數擴展缺口)")
        st.markdown("🟠 **Medium:** Review prior knowledge on fractions")
        if st.button("Assign demo action"):
            st.success("Action logged (demo mode)")

st.divider()
st.caption("HK bilingual prototype • In production: class-wide heatmaps, trend lines, LLM-generated plans. All tags have name_en + name_yue.")
