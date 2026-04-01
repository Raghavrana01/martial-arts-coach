# 🥋 AI Martial Arts Coach

A multi-agent AI coaching system for Muay Thai, Boxing, and Kickboxing — built with CrewAI, Gemini 2.5, and Streamlit.

## What it does
The **AI Martial Arts Coach** is a comprehensive training companion delivered through a modern Streamlit web UI. It features a wise, "Sensei-like" personality that provides expert guidance on technical skills, mindset, and physical preparation. Most importantly, the coach **remembers you across sessions**, maintaining a persistent understanding of your progress, injuries, and goals.

## Multi-Agent Architecture
The system utilizes a sequential CrewAI pipeline of 6 specialized agents. Each agent builds upon the output of the previous one to provide a cohesive, multi-disciplinary response:

1.  **Master Chen (Technique Coach)**: Focuses on striking mechanics, footwork, and defensive form.
2.  **Sensei Ryu (Philosopher)**: Integrates mindset, discipline, and the "warrior's path" using Eastern philosophy and Stoicism.
3.  **Coach Maya (Training Planner)**: Designs structured weekly training plans with duration and intensity.
4.  **Dr. Kai (Nutritionist)**: Provides practical fuel and hydration advice tailored to a fighter's needs.
5.  **Dr. Santos (Sports Medicine Doctor)**: Offers safety-first guidance on load management and injury awareness.
6.  **Master Coach Coordinator (Synthesizer)**: Merges all specialist inputs into one unified, clear coaching voice.

## Long-Term Memory
The application features a built-in memory system managed by `memory_manager.py`. It automatically extracts key facts (such as your training background, current goals, and active injuries) from your conversations and persists them in `memory.json`. This allows the coaching team to provide increasingly personalized advice the more you interact with them.

## Tech Stack
- **Python 3**
- **CrewAI**: Multi-agent orchestration framework.
- **Google Gemini 2.5 Flash**: The primary LLM powering all agents.
- **Streamlit**: For the interactive web interface.
- **python-dotenv**: For secure environment variable management.

## Setup
1.  **Create and activate a virtual environment**:
    ```bash
    python -m venv env
    .\env\Scripts\Activate.ps1  # Windows
    source env/bin/activate     # macOS/Linux
    ```
2.  **Install dependencies**:
    ```bash
    pip install streamlit crewai litellm python-dotenv
    ```
3.  **Configure environment variables**:
    Create a `.env` file in the project root with your API keys:
    ```env
    GEMINI_API_KEY=your_gemini_api_key_here
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```
4.  **Run the application**:
    ```bash
    streamlit run app.py
    ```

## Project Structure
- **app.py**: The Streamlit frontend and main application logic.
- **crew_coach.py**: Defines the CrewAI agents, tasks, and sequential pipeline.
- **memory_manager.py**: Handles fact extraction via Gemini and JSON-based memory storage.
- **.env**: Local configuration for API keys (not committed to version control).
- **memory.json**: Persistent storage for user-specific training facts.

## Disclaimer
This AI coach is intended for educational and motivational purposes only. It is not a substitute for professional coaching or medical advice. Always consult with a qualified trainer or healthcare provider before beginning a new exercise program or treating an injury.
