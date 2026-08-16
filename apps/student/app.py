import streamlit as st
import httpx
import os

st.set_page_config(page_title="Socratic Chat", page_icon="🧠")
st.title("🧠 Socratic Learning Lab — 蘇格拉底學習實驗室")
st.caption("Talk through ideas (English + 粵語). We tag your thinking bottlenecks in real time.")

# Config for deployed vs local
DEFAULT_DEPLOYED = "https://socratic-edtech.onrender.com"
DEFAULT_LOCAL = "http://localhost:8000"

with st.sidebar:
    st.header("Connection")
    env = st.selectbox("Backend", ["Deployed (Render)", "Local"], index=0)
    API_URL = DEFAULT_DEPLOYED if "Deployed" in env else DEFAULT_LOCAL
    st.caption(f"Using: {API_URL}")
    st.caption("If deployed sleeps, first load may take 30-60s.")

    lang = st.selectbox("Language / 語言", ["bilingual", "en", "yue"], index=0)
    st.session_state["lang_pref"] = lang

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tags"):
            st.caption(f"**Tags:** {', '.join(msg['tags'])}")

if prompt := st.chat_input("What's on your mind? / 你有咩問題？"):
    st.session_state.messages.append({"role": "student", "content": prompt})
    with st.chat_message("student"):
        st.markdown(prompt)

    try:
        resp = httpx.post(
            f"{API_URL}/chat/message",
            json={"content": prompt, "language": st.session_state.get("lang_pref", "bilingual")},
            timeout=60
        )
        data = resp.json()
        assistant_msg = data["message"]

        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_msg["content"],
            "tags": assistant_msg.get("bottleneck_tags", [])
        })

        with st.chat_message("assistant"):
            st.markdown(assistant_msg["content"])
            if assistant_msg.get("bottleneck_tags"):
                st.caption(f"**Cognitive bottlenecks detected / 認知瓶頸:** {', '.join(assistant_msg['bottleneck_tags'])}")

        if data.get("suggested_next_question"):
            st.info(f"💡 Try thinking about: *{data['suggested_next_question']}*")

    except Exception as e:
        st.error(f"Backend not running or error: {e}")
        # Fallback demo bilingual
        fallback = "What makes you say that? Can you give a concrete example?\n\n[粵語] 你點解咁講？可唔可以講個具體例子？"
        st.session_state.messages.append({
            "role": "assistant",
            "content": fallback,
            "tags": ["conceptual_misunderstanding"]
        })
        with st.chat_message("assistant"):
            st.markdown(fallback)
            st.caption("**Tags:** conceptual_misunderstanding")
