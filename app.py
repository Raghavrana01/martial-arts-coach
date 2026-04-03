import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
import base64
from io import BytesIO

# Load environment variables
load_dotenv(Path(__file__).resolve().parent / ".env")

from crew_coach import (
    run_agent_pipeline,
)
from memory_manager import extract_facts, load_memory, save_memory, get_memory_file
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

if "user_name" not in st.session_state:
    st.session_state.user_name = "guest"

if "user_memory" not in st.session_state:
    st.session_state.user_memory = load_memory(st.session_state.user_name)

if "current_plan" not in st.session_state:
    st.session_state.current_plan = ""

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-title">🥋 SENSEI AI</div>', unsafe_allow_html=True)
    
    if st.session_state.user_name != "guest":
        st.markdown(f'<div style="color: #FFD700; text-align: center; margin-bottom: 1rem;">Welcome back, {st.session_state.user_name}!</div>', unsafe_allow_html=True)

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
        memory_file = get_memory_file(st.session_state.user_name)
        if memory_file.exists():
            os.remove(memory_file)
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
        user_name = st.text_input("Your Username", placeholder="Enter your name...")
        exp_level = st.selectbox("What is your experience level?", ["Beginner", "Intermediate", "Advanced"])
        goal = st.selectbox("What is your primary goal?", ["Get Fit", "Compete", "Self Defence", "General Martial Arts"])
        styles = st.multiselect("What styles do you train?", ["Muay Thai", "Boxing", "Kickboxing", "MMA", "Other"])
        
        submitted = st.form_submit_button("Start Training")
        if submitted:
            final_username = user_name.strip() if user_name.strip() else "guest"
            onboarding_data = {
                "experience_level": exp_level,
                "primary_goal": goal,
                "styles_trained": ", ".join(styles) if styles else "Not specified"
            }
            save_memory(onboarding_data, final_username)
            st.session_state.user_name = final_username
            st.session_state.user_memory = onboarding_data
            st.success(f"Your profile is recorded, {final_username}. Welcome, student.")
            st.rerun()
    st.stop()

# --- Main App Tabs ---
tab1, tab2, tab3 = st.tabs(["🥋 Dojo Chat", "📋 Training Plan", "👁️ Technique Vision"])

# --- Tab 1: Dojo Chat ---
with tab1:
    st.markdown('<h2 style="color: #FFD700; text-align: center;">Combat Sports Dojo</h2>', unsafe_allow_html=True)

    # 1. Render history first
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

    # 2. Input at bottom
    question = st.chat_input("Ask your coach anything...")

    if question:
        user_text = question.strip()
        
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
        
        # Render both user and coach bubbles IMMEDIATELY inline
        st.markdown(f'<div class="user-message">{user_text}</div>', unsafe_allow_html=True)
        st.markdown(f"""
            <div class="coach-message">
                <b>🥋 Sensei:</b><br>{reply}
                <div class="agent-tags">{agents_line}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
        
        # Append to state after rendering
        st.session_state.messages.append({"role": "user", "content": user_text})
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply,
                "agents": agents_line,
            },
        )

        # Background memory update
        try:
            new_facts = extract_facts(st.session_state.messages, st.session_state.user_name)
            if new_facts:
                st.session_state.user_memory.update(new_facts)
                save_memory(st.session_state.user_memory, st.session_state.user_name)
                print(f"Memory updated and saved for {st.session_state.user_name}")
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

# --- Tab 3: Technique Vision ---
with tab3:
    st.markdown('<h2 style="color: #FFD700; text-align: center;">Technique Vision Analysis</h2>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload a photo of your martial arts stance or technique",
        type=["jpg", "jpeg", "png"],
        help="Upload a clear photo showing your stance, guard, or technique"
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        st.image(uploaded_file, caption="Your technique",width=600)
        
        # Analyze button
        if st.button("🔍 Analyze Technique", key="analyze_vision"):
            with st.spinner("👁️ Master Chen is analyzing your technique..."):
                try:
                    # Configure Gemini
                    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
                    model = genai.GenerativeModel('gemini-2.5-flash')
                    
                    # Convert image to bytes
                    image_bytes = uploaded_file.getvalue()
                    
                    # Prepare the vision analysis prompt
                    vision_prompt = """
                    You are Master Chen, a veteran martial arts technique coach with 40 years of experience in Muay Thai, Boxing, Kickboxing, and various traditional martial arts.
                    
                    Analyze this martial arts technique/stance photo and provide a detailed technical assessment focusing on:
                    1. Stance and balance
                    2. Guard position and defensive structure
                    3. Body positioning and alignment
                    4. Any technical errors or areas for improvement
                    5. Specific corrections that would improve the technique
                    
                    Be specific, technical, and actionable in your analysis. Focus on what you can actually see in the image.
                    """
                    
                    # Create the content parts for Gemini
                    image_part = {
                        "mime_type": uploaded_file.type,
                        "data": base64.b64encode(image_bytes).decode()
                    }
                    
                    # Get vision analysis from Gemini
                    response = model.generate_content([
                        vision_prompt,
                        image_part
                    ])
                    
                    vision_analysis = response.text
                    
                    # Now pass this analysis to Master Chen (technique agent) for coaching feedback
                    coaching_prompt = f"""
                    A student has uploaded a photo of their martial arts technique. Here is what Gemini Vision analysis revealed about their technique:
                    
                    {vision_analysis}
                    
                    Based on this visual analysis, provide specific coaching feedback to help the student improve. Focus on:
                    1. The most critical corrections needed
                    2. Specific drills or exercises to fix the identified issues
                    3. Key cues to remember when practicing this technique
                    4. How these corrections will improve their overall performance
                    
                    Speak as Master Chen - direct, technical, and encouraging. Give actionable advice they can implement immediately.
                    """
                    
                    # Use the existing crew system to get Master Chen's coaching
                    activated, coaching_reply = run_agent_pipeline(
                        coaching_prompt,
                        conversation_history=[],
                        user_memory=str(st.session_state.user_memory)
                    )
                    
                    # Display the results in coach-message style
                    st.markdown('<h3 style="color: #FFD700; margin-top: 2rem;">📸 Vision Analysis</h3>', unsafe_allow_html=True)
                    st.markdown(f'<div class="plan-box">{vision_analysis}</div>', unsafe_allow_html=True)
                    
                    st.markdown('<h3 style="color: #FFD700; margin-top: 2rem;">🥋 Master Chen\'s Coaching</h3>', unsafe_allow_html=True)
                    st.markdown(f"""
                        <div class="coach-message">
                            <b>🥋 Master Chen:</b><br>{coaching_reply}
                            <div class="agent-tags">{" → ".join(activated) if activated else "Technique Coach"}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    st.markdown('<div style="clear: both;"></div>', unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Error analyzing technique: {str(e)}")
                    
    else:
        st.markdown('<div style="text-align: center; color: #888; margin-top: 3rem;">📷 Upload a photo to begin your technique analysis</div>', unsafe_allow_html=True)
