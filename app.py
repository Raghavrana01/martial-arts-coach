"""
Streamlit UI for the CrewAI martial arts coaching crew (crew_coach.run_agent_pipeline).
Run: streamlit run app.py
"""

from __future__ import annotations

import html
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")

from crew_coach import (
    run_agent_pipeline,
)

st.set_page_config(
    page_title="AI Martial Arts Coach",
    page_icon="🥋",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap');
    html, body, [class*="css"] {
        font-family: 'Noto Sans', sans-serif;
    }
    .stApp {
        background: radial-gradient(ellipse at 20% 0%, #2a1810 0%, transparent 50%),
                    radial-gradient(ellipse at 80% 100%, #0f1a24 0%, transparent 45%),
                    linear-gradient(175deg, #0a0a0c 0%, #121418 40%, #0c0e12 100%);
        color: #e8e4df;
    }
    .block-container {
        padding-top: 1.5rem;
        max-width: 52rem;
    }
    h1 {
        font-weight: 700 !important;
        letter-spacing: 0.02em;
        text-shadow: 0 2px 24px rgba(201, 162, 39, 0.25);
        border-bottom: 1px solid rgba(201, 162, 39, 0.35);
        padding-bottom: 0.75rem;
        margin-bottom: 1.25rem !important;
    }
    div[data-testid="stChatMessage"] {
        background: rgba(255, 255, 255, 0.03) !important;
        border: 1px solid rgba(201, 162, 39, 0.12) !important;
        border-radius: 14px !important;
        margin-bottom: 0.75rem !important;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.35);
    }
    div[data-testid="stChatMessage"] p {
        color: #e8e4df !important;
    }
    .agent-meta {
        color: #7a7874 !important;
        font-size: 0.78rem !important;
        margin-top: 0.35rem !important;
        letter-spacing: 0.01em;
    }
    div[data-testid="stForm"] {
        border: 1px solid rgba(201, 162, 39, 0.2);
        border-radius: 12px;
        padding: 0.75rem 1rem 1rem;
        background: rgba(0, 0, 0, 0.35);
    }
    .stTextInput input {
        background: rgba(255, 255, 255, 0.06) !important;
        color: #f0ece6 !important;
        border: 1px solid rgba(201, 162, 39, 0.25) !important;
        border-radius: 8px !important;
    }
    .stButton button {
        background: linear-gradient(180deg, #8b6914 0%, #5c4a0f 100%) !important;
        color: #f5f0e4 !important;
        border: 1px solid rgba(201, 162, 39, 0.5) !important;
        font-weight: 600 !important;
    }
    .stButton button:hover {
        border-color: #d4af37 !important;
        box-shadow: 0 0 12px rgba(212, 175, 55, 0.35);
    }
</style>
""",
    unsafe_allow_html=True,
)

st.title("🥋 AI Martial Arts Coach")

if "messages" not in st.session_state:
    st.session_state.messages = []

if not os.environ.get("GROQ_API_KEY"):
    st.error("Set **GROQ_API_KEY** in your `.env` file next to `app.py`.")
    st.stop()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg["role"] == "assistant" and msg.get("agents"):
            st.markdown(
                f'<p class="agent-meta">Agents: {html.escape(msg["agents"])}</p>',
                unsafe_allow_html=True,
            )

with st.form("chat_form", clear_on_submit=True):
    col_text, col_send = st.columns([5, 1])
    with col_text:
        question = st.text_input(
            "Your question",
            label_visibility="collapsed",
            placeholder="Ask about technique, training, nutrition, mindset…",
        )
    with col_send:
        submitted = st.form_submit_button("Send")

if submitted and question.strip():
    user_text = question.strip()
    st.session_state.messages.append({"role": "user", "content": user_text})
    conversation_history = st.session_state.messages[-6:]

    try:
        with st.spinner("Your coaches are deliberating..."):
            activated, reply = run_agent_pipeline(
                user_text,
                conversation_history=conversation_history,
            )
    except Exception as e:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": f"Something went wrong: {e}",
                "agents": "",
            }
        )
        st.rerun()

    agents_line = " → ".join(activated) if activated else "Crew"
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
            "agents": agents_line,
        },
    )
    st.rerun()
