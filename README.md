# 🥋 AI Martial Arts Coach

> *"The successful warrior is the average man, with laser-like focus."* — Bruce Lee


Designed to demonstrate real multi-agent architecture, RAG pipelines, and production deployment.


A team of 6 AI specialists who collaborate in real-time to coach you in Muay Thai, Boxing, and Kickboxing. Not a chatbot. A coaching system that thinks, remembers, and grows with you.

🚀 **[Try It Live →](https://martial-arts-coach-kdjjzmtrvapwl3zcc9stje.streamlit.app)**

---

## What Makes This Different

Most AI tools give you one generic response. This system routes your question to the right specialists, runs them in sequence — each one building on the last — then synthesizes everything into one unified coaching voice.

Ask about your jab. You get technique from Master Chen, mental context from Sensei Ryu, a drill plan from Coach Maya, recovery advice from Dr. Kai, and one clean response that sounds like a single wise sensei who consulted his entire staff before speaking.

**And it remembers you.** Tell it you've been training 6 months, that your left hook is weak, that you want to compete. Come back tomorrow — it already knows.

---

## Features

**🧠 Multi-Agent Intelligence**
Six specialist AI agents collaborate on every response. Each reads the previous agent's output and builds on it — true sequential reasoning, not parallel noise.

**📚 RAG Knowledge Base**
12 detailed martial arts coaching documents power the system. Technique breakdowns, fight strategy, conditioning protocols, nutrition guides, mental game frameworks — all retrieved semantically before the agents speak.

**💾 Long-Term Memory**
The coach extracts facts from your conversations and stores them. Your training background, goals, injuries, and techniques practiced persist across every session. The longer you use it, the sharper it gets.

**🎯 Personalised Onboarding**
New users complete a quick dojo intake — experience level, training goals, styles practiced. This profile immediately personalises every response from the first message.

**📋 Training Plan Generator**
Input your weekly schedule and goals. The system generates a specific, day-by-day training program with exact drills, round counts, and intensity levels. Downloadable as a text file.

**⚔️ Unified Sensei Voice**
The final response always comes through the Master Coach Coordinator — synthesised into flowing paragraphs, never bullet points, warm but demanding. Like a real sensei who has seen a thousand students walk through the door.

---

## How It Works

```
Your Question
     ↓
Orchestrator decides which agents are needed
     ↓
Master Chen → Sensei Ryu → Coach Maya → Dr. Kai → Dr. Santos
(each agent reads the previous one's output)
     ↓
RAG retrieves relevant knowledge from ChromaDB
     ↓
Master Coach Coordinator synthesizes everything
     ↓
One unified coaching response
```

---

## Agent Roster

| Agent | Personality | Specialty |
|-------|------------|-----------|
| **Master Chen** | Strict, precise, no-nonsense | Striking mechanics, footwork, defensive form |
| **Sensei Ryu** | Calm, powerful, philosophical | Mindset, discipline, Eastern wisdom, Stoicism |
| **Coach Maya** | Military precision | Day-by-day training plans, periodization |
| **Dr. Kai** | Practical, direct | Fighter nutrition, hydration, recovery |
| **Dr. Santos** | Ringside experience | Injury awareness, load management |
| **Master Coach Coordinator** | Warm, wise, unified | Synthesizes all inputs into one sensei voice |

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3.11 | Core language |
| CrewAI | Multi-agent orchestration framework |
| Google Gemini 2.5 Flash | LLM powering all agents |
| ChromaDB | Vector database for RAG |
| Sentence Transformers | Semantic embeddings (all-MiniLM-L6-v2) |
| Streamlit | Web UI |
| python-dotenv | Secure API key management |

---

## Setup

**1. Clone and create virtual environment:**
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
pip install streamlit crewai litellm python-dotenv chromadb sentence-transformers google-generativeai
```

**3. Add your API keys** — create a `.env` file:
```env
GEMINI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```
Get a free key at [aistudio.google.com](https://aistudio.google.com)

**4. Run:**
```bash
streamlit run app.py
```

The knowledge base builds automatically on first run.

---

## Project Structure

```
martial-arts-coach/
├── app.py                     # Streamlit UI, onboarding, training plan tab
├── crew_coach.py              # CrewAI agents, tasks, sequential pipeline
├── memory_manager.py          # Long-term memory extraction and storage
├── knowledge_base.py          # ChromaDB vector store and semantic search
├── martial_arts_knowledge.py  # 12 detailed martial arts coaching documents
├── setup_rag.py               # Knowledge base initialization script
├── .env.example               # API key template
└── memory.json                # Auto-generated training profile (gitignored)
```

---
## Recent Updates
- Fixed first-message rendering bug — responses now appear instantly without requiring a second prompt
- Mobile sidebar collapsed by default with compact memory display
- RAG fallback to LLM knowledge when no relevant documents found
- Per-user memory files so multiple users maintain separate profiles

## What's Next
- Video / image technique analysis via Gemini Vision
- Krav Maga and expanded striking arts knowledge base
- Expanded RAG corpus with sport-specific documents

## Disclaimer

For educational and motivational purposes. Not a substitute for a real coach, doctor, or emergency care.

---
