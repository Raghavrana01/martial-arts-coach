# 🥋 AI Martial Arts Coach

A multi-agent AI coaching system for Muay Thai, Boxing, and Kickboxing — built with CrewAI, Google Gemini 2.5, and Streamlit.

> *"The successful warrior is the average man, with laser-like focus."* — Bruce Lee

---

## What It Does

This is not a chatbot. It's a team of AI specialists who collaborate to answer your questions — then a master coordinator who distills their combined wisdom into one unified coaching voice.

Ask about technique, mindset, training plans, nutrition, or injuries. The system decides which experts you need, runs them in sequence, and delivers a single, coherent response — as if a wise sensei had consulted their entire staff before speaking.

The coach also **remembers you**. Tell it your goals, your injuries, your training background — and it carries that knowledge into every future session.

---

## Multi-Agent Architecture

Six CrewAI agents run sequentially. Each one reads the previous agent's output and builds on it — true collaboration, not parallel monologues.

| Agent | Personality | Specialty |
|-------|------------|-----------|
| **Master Chen** | Strict, precise, no-nonsense | Striking mechanics, footwork, defensive form |
| **Sensei Ryu** | Calm, powerful, philosophical | Mindset, discipline, Eastern wisdom, Stoicism |
| **Coach Maya** | Military precision | Weekly training plans, intensity, periodization |
| **Dr. Kai** | Practical, direct | Fighter nutrition, hydration, recovery meals |
| **Dr. Santos** | Safety-first, measured | Injury awareness, load management, red flags |
| **Master Coach Coordinator** | Warm, wise, unified | Synthesizes all inputs into one sensei voice |

---

## Long-Term Memory

The coach learns who you are over time. After every conversation, `memory_manager.py` extracts key facts — training experience, goals, techniques practiced, injuries — and saves them to `memory.json`.

Next session, the coach already knows you. The longer you use it, the more personalized it becomes.

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3 | Core language |
| CrewAI | Multi-agent orchestration |
| Google Gemini 2.5 Flash | LLM powering all agents |
| Streamlit | Web UI |
| python-dotenv | Secure API key management |

---

## Setup

**1. Clone the repo and create a virtual environment:**
```bash
git clone https://github.com/Raghavrana01/martial-arts-coach.git
cd martial-arts-coach
python -m venv env

# Windows
.\env\Scripts\Activate.ps1

# macOS/Linux
source env/bin/activate
```

**2. Install dependencies:**
```bash
pip install streamlit crewai litellm python-dotenv
```

**3. Configure your API keys:**

Create a `.env` file in the project root:
```env
GEMINI_API_KEY=your_gemini_api_key_here
GOOGLE_API_KEY=your_gemini_api_key_here
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

**4. Run:**
```bash
streamlit run app.py
```

---

## Project Structure

```
martial-arts-coach/
├── app.py              # Streamlit frontend and main application logic
├── crew_coach.py       # CrewAI agents, tasks, and sequential pipeline
├── memory_manager.py   # Fact extraction and persistent memory storage
├── .env                # API keys (never committed to version control)
├── .env.example        # Template for environment setup
└── memory.json         # Auto-generated: stores your training profile
```

---

## Disclaimer

This AI coach is for educational and motivational purposes only. It is not a substitute for professional coaching, medical advice, or emergency care. For injuries, pain, or health concerns — see a real professional.
