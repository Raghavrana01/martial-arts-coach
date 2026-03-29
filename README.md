# Martial Arts Coach

An **AI martial arts coaching** CLI that answers questions about technique, mindset, training plans, nutrition, and injury-aware guidance. It uses several specialist “agents” behind one unified voice, coordinated by an orchestrator and merged by a synthesizer.

## Multi-agent architecture

Each turn works like a small pipeline:

1. **Orchestrator** — Reads your message and returns a comma-separated list of which specialists to involve (e.g. `PLANNER,NUTRITION`). It can pick **one or many** agents, ordered by relevance.

2. **Five specialist agents** — Each has its own system prompt and role:
   - **TECHNIQUE** — Muay Thai–style striking: stance, guard, drills, form, safety.
   - **PHILOSOPHY** — Mindset, discipline, fear, and life lessons (Eastern philosophy, Stoicism, Bruce Lee–style wisdom).
   - **PLANNER** — Weekly combat-sports conditioning: day-by-day structure, duration, intensity.
   - **NUTRITION** — Meals, weight management, hydration, recovery, sleep, concrete food ideas.
   - **DOCTOR** — Sports-medicine style guidance: possible causes, first aid, recovery, when to see a clinician (no definitive diagnosis).

   Specialists run **in sequence**. After the first, each sees the **previous specialist’s reply** as extra context so advice can build on what came before.

3. **Safety pass** — If your message mentions pain, injury, soreness, swelling, or similar medical wording, **DOCTOR** is added to the run if the orchestrator did not already include it.

4. **Synthesizer** — Takes all specialist outputs plus your original question and produces **one** clear, structured answer in a **single coach voice**, without naming the internal agents.

All of those steps use the same underlying chat model via the Groq API (see below).

## Tech stack

| Piece | Choice |
|--------|--------|
| Language | **Python 3** |
| LLM API | **[Groq](https://console.groq.com/)** (`groq` Python SDK) |
| Model | **Meta Llama 3** — `llama-3.3-70b-versatile` |
| Config | **`python-dotenv`** — loads `GROQ_API_KEY` from a `.env` file |

## Install

1. **Clone or copy** this project and open a terminal in the project folder.

2. **Create and activate a virtual environment** (recommended):

   ```powershell
   python -m venv env
   .\env\Scripts\Activate.ps1
   ```

   On macOS/Linux:

   ```bash
   python3 -m venv env
   source env/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install groq python-dotenv
   ```

4. **Configure the API key** — Create a `.env` file in the project root (this repo’s `.gitignore` keeps it out of git):

   ```env
   GROQ_API_KEY=your_groq_api_key_here
   ```

   Get a key from the [Groq Console](https://console.groq.com/).

## Run

From the project directory, with the venv activated:

```bash
python coach.py
```

Type your question at the `You:` prompt. The app prints which agents were selected, then the **synthesized** reply. Use an empty line or `quit` / `exit` / `q` to leave.

## Disclaimer

This tool is for **education and general coaching ideas**, not a substitute for a qualified coach, doctor, or emergency care. For pain, injury, or medical concerns, follow the app’s reminders and seek professional care when appropriate.
