import streamlit as st
import httpx
import os

st.set_page_config(page_title="Socratic Chat", page_icon="🧠")
st.title("🧠 Socratic Learning Lab")
st.caption("Talk through ideas. We tag your thinking bottlenecks in real time.")

API_URL = "http://localhost:8000"

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("tags"):
            st.caption(f"**Tags:** {', '.join(msg['tags'])}")

if prompt := st.chat_input("What's on your mind?"):
    st.session_state.messages.append({"role": "student", "content": prompt})
    with st.chat_message("student"):
        st.markdown(prompt)

    try:
        resp = httpx.post(
            f"{API_URL}/chat/message",
            json={"content": prompt, "role": "student"},
            timeout=30
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
                st.caption(f"**Cognitive bottlenecks detected:** {', '.join(assistant_msg['bottleneck_tags'])}")

        if data.get("suggested_next_question"):
            st.info(f"💡 Try thinking about: *{data['suggested_next_question']}*")

    except Exception as e:
        st.error(f"Backend not running or error: {e}")
        # Fallback demo
        st.session_state.messages.append({
            "role": "assistant",
            "content": "What makes you say that? Can you give a concrete example?",
            "tags": ["conceptual_misunderstanding"]
        })
        with st.chat_message("assistant"):
            st.markdown("What makes you say that? Can you give a concrete example?")
            st.caption("**Tags:** conceptual_misunderstanding")
