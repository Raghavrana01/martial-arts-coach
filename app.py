import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).resolve().parent / ".env")

from crew_coach import (
    run_agent_pipeline,
)
from memory_manager import extract_facts, load_memory, save_memory, MEMORY_FILE
from knowledge_base import knowledge_base_exists, build_knowledge_base
from martial_arts_knowledge import KNOWLEDGE_DOCUMENTS

# Silent RAG initialization on startup
try:
    if not knowledge_base_exists():
        build_knowledge_base(KNOWLEDGE_DOCUMENTS)
except Exception:
    pass

# Page Config
st.set_page_config(
    page_title="Martial Arts AI Coach",
    page_icon="🥋",
    layout="wide",
)

# Premium Dark Martial Arts Theme CSS
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0a0a0a;
        color: #e0e0e0;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #111111;
        border-right: 1px solid #FFD700;
    }
    
    .sidebar-title {
        color: #FFD700;
        font-size: 1.8rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px #8B0000;
    }
    
    /* Chat Bubbles */
    .user-message {
        background-color: #8B0000;
        color: white;
        padding: 1rem;
        border-radius: 15px 15px 0px 15px;
        margin: 1rem 0;
        float: right;
        width: 85%;
        border: 1px solid #4a0000;
    }
    
    .coach-message {
        background-color: #1e1e1e;
        color: #e0e0e0;
        padding: 1rem;
        border-radius: 15px 15px 15px 0px;
        margin: 1rem 0;
        float: left;
        width: 85%;
        border-left: 5px solid #FFD700;
    }
    
    .agent-tags {
        color: #FFD700;
        font-size: 0.7rem;
        font-style: italic;
        margin-top: 0.5rem;
    }
    
    /* Buttons */
    .stButton>button {
        background-color: #FFD700;
        color: black;
        border-radius: 5px;
        border: none;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        background-color: #DAA520;
        color: white;
        box-shadow: 0 0 10px #FFD700;
    }
    
    /* Input Styling */
    .stTextInput>div>div>input {
        background-color: #1e1e1e;
        color: white;
        border: 1px solid #FFD700;
    }
    
    .plan-box {
        background-color: #111111;
        border: 1px solid #FFD700;
        padding: 20px;
        border-radius: 10px;
        color: #e0e0e0;
        white-space: pre-wrap;
    }

    /* Hide default streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# Initialize Session States
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_memory" not in st.session_state:
    st.session_state.user_memory = load_memory()

if "current_plan" not in st.session_state:
    st.session_state.current_plan = ""

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🥋 SENSEI AI</div>', unsafe_allow_html=True)
    
    # Memory Section
    st.markdown("### 🏺 Coach Remembers:")
    if st.session_state.user_memory:
        for category, info in st.session_state.user_memory.items():
            if info:
                st.markdown(f"**{category.replace('_', ' ').title()}**: {info}")
    else:
        st.info("No prior training memory yet.")
    
    st.divider()
    
    # Actions
    if st.button("🗑️ Clear Memory"):
        if MEMORY_FILE.exists():
            os.remove(MEMORY_FILE)
        st.session_state.user_memory = {}
        st.success("Memory purged.")
        st.rerun()
        
    if st.button("🔄 New Session"):
        st.session_state.messages = []
        st.success("Conversation cleared.")
        st.rerun()

# --- Onboarding Screen ---
if not st.session_state.user_memory:
    st.markdown('<h2 style="color: #FFD700; text-align: center;">Welcome to the Dojo</h2>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center;">Before we begin your training, Sensei needs to know who you are.</p>', unsafe_allow_html=True)
    
    with st.form("onboarding_form"):
        exp_level = st.selectbox("What is your experience level?", ["Beginner", "Intermediate", "Advanced"])
        goal = st.selectbox("What is your primary goal?", ["Get Fit", "Compete", "Self Defence", "General Martial Arts"])
        styles = st.multiselect("What styles do you train?", ["Muay Thai", "Boxing", "Kickboxing", "MMA", "Other"])
        
        submitted = st.form_submit_button("Start Training")
        if submitted:
            onboarding_data = {
                "experience_level": exp_level,
                "primary_goal": goal,
                "styles_trained": ", ".join(styles) if styles else "Not specified"
            }
            save_memory(onboarding_data)
            st.session_state.user_memory = onboarding_data
            st.success("Your profile is recorded. Welcome, student.")
            st.rerun()
    st.stop()

# --- Main App Tabs ---
tab1, tab2 = st.tabs(["🥋 Dojo Chat", "📋 Training Plan"])

# --- Tab 1: Dojo Chat ---
with tab1:
    st.markdown('<h2 style="color: #FFD700; text-align: center;">Combat Sports Dojo</h2>', unsafe_allow_html=True)

    chat_container = st.container()

    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f"""
                    <div class="coach-message">
                        <b>🥋 Sensei:</b><br>{msg["content"]}
                        <div class="agent-tags">{msg.get("agents", "Crew")}</div>
                    </div>
                    """, unsafe_allow_html=True)
        st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)

    # Input Area
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([8, 2])
        with col1:
            question = st.text_input("", placeholder="Ask your coach anything...", label_visibility="collapsed")
        with col2:
            submitted = st.form_submit_button("Ask Sensei")

        if submitted and question.strip():
            user_text = question.strip()
            st.session_state.messages.append({"role": "user", "content": user_text})
            
            # Prepare context for pipeline
            conversation_history = st.session_state.messages[-6:]
            user_memory_str = str(st.session_state.user_memory)
            
            try:
                with st.spinner("⚔️ Your coaches are deliberating..."):
                    activated, reply = run_agent_pipeline(
                        user_text,
                        conversation_history=conversation_history,
                        user_memory=user_memory_str,
                    )
            except Exception as e:
                reply = f"The flow of energy was interrupted: {e}"
                activated = ["Error"]

            agents_line = " → ".join(activated) if activated else "Sensei"
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": reply,
                    "agents": agents_line,
                },
            )

            # Background memory update
            try:
                new_facts = extract_facts(st.session_state.messages)
                if new_facts:
                    st.session_state.user_memory.update(new_facts)
                    save_memory(st.session_state.user_memory)
                    print("Memory updated and saved to memory.json")
            except Exception as e:
                print(f"Failed to update memory: {e}")

            st.rerun()

# --- Tab 2: Training Plan ---
with tab2:
    st.markdown('<h2 style="color: #FFD700; text-align: center;">Personalized Training Plan</h2>', unsafe_allow_html=True)
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            days = st.slider("Training days per week", 1, 7, 3)
            duration = st.number_input("Session length (minutes)", 30, 180, 60, 15)
        with col2:
            focus = st.text_input("Specific focus area", placeholder="e.g. Footwork, Power, Conditioning...")
            
        generate = st.button("Generate My Plan")
        
        if generate:
            plan_prompt = (
                f"Create a detailed weekly training plan for a {st.session_state.user_memory.get('experience_level', 'student')} "
                f"martial artist. They train {days} days a week for {duration} minutes per session. "
                f"Focus area: {focus if focus else 'General fundamentals'}. "
                f"Context: {st.session_state.user_memory}"
            )
            
            try:
                with st.spinner("⚔️ Crafting your specialized regime..."):
                    _, reply = run_agent_pipeline(
                        plan_prompt,
                        conversation_history=[],
                        user_memory=str(st.session_state.user_memory)
                    )
                    st.session_state.current_plan = reply
            except Exception as e:
                st.error(f"Failed to generate plan: {e}")

        if st.session_state.current_plan:
            st.markdown("### 📜 Your Weekly Regime")
            st.markdown(f'<div class="plan-box">{st.session_state.current_plan}</div>', unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Download Plan",
                data=st.session_state.current_plan,
                file_name="martial_arts_training_plan.txt",
                mime="text/plain"
            )
