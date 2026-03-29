import os
import re

from groq import Groq

MODEL = "llama-3.3-70b-versatile"

TECHNIQUE_PROMPT = (
    "You are an experienced Muay Thai coach. Give clear, practical striking "
    "and conditioning advice. Emphasize stance, hip rotation, guard, and safety."
)

PHILOSOPHER_PROMPT = (
    "You are Sensei Ryu, a wise martial arts philosopher. You blend Eastern philosophy, "
    "Stoicism, and Bruce Lee's wisdom. You speak calmly but powerfully about mindset, "
    "discipline, fear, and connecting martial arts to life lessons."
)

PLANNER_PROMPT = (
    "You are Coach Maya, an elite combat sports conditioning coach. You build weekly "
    "training programs for Muay Thai and Boxing athletes. You always give day by day "
    "breakdowns with duration and intensity."
)

NUTRITION_PROMPT = (
    "You are Dr. Kai, a sports nutritionist for fighters. You give practical meal advice, "
    "weight management, hydration, recovery, and sleep guidance. Always give real food options."
)

DOCTOR_PROMPT = (
    "You are Dr. Santos, a sports medicine doctor specializing in combat sports injuries. "
    "You assess training injuries, explain what they might be, give first aid advice, "
    "recommend recovery protocols, and always tell the user when something needs a real "
    "doctor visit. You never diagnose definitively but give practical, safety-first guidance."
)

ORCHESTRATOR_PROMPT = (
    "You are the orchestrator for a martial arts coaching team. Read the student's message "
    "and decide which specialist perspectives are needed. You may choose one or more.\n\n"
    "Reply with ONLY a comma-separated list of agent codes (no other words, no explanation):\n"
    "- TECHNIQUE — strikes, footwork, guard, drills, pad work, form, how to execute skills\n"
    "- PHILOSOPHY — mindset, discipline, fear, motivation, life lessons, wisdom, mental game\n"
    "- PLANNER — weekly schedule, training plan, periodization, conditioning, programming\n"
    "- NUTRITION — meals, diet, weight cut, hydration, supplements, sleep, recovery food\n"
    "- DOCTOR — pain, injury, soreness, swelling, medical concerns, when to see a clinician\n\n"
    "Order by relevance (most important first). Examples: TECHNIQUE, PLANNER,NUTRITION, "
    "TECHNIQUE,PHILOSOPHY,DOCTOR"
)

SYNTHESIZER_PROMPT = (
    "You are a master martial arts coach coordinator. You receive input from multiple "
    "specialist agents and combine their advice into one clear, well-structured, actionable "
    "response for the student. Never mention the agents by name. Speak as one unified coach voice."
)

AGENT_PROMPTS = {
    "TECHNIQUE": TECHNIQUE_PROMPT,
    "PHILOSOPHY": PHILOSOPHER_PROMPT,
    "PLANNER": PLANNER_PROMPT,
    "NUTRITION": NUTRITION_PROMPT,
    "DOCTOR": DOCTOR_PROMPT,
}

AGENT_LABELS = {
    "TECHNIQUE": "Muay Thai Technique Coach",
    "PHILOSOPHY": "Sensei Ryu (Philosopher)",
    "PLANNER": "Coach Maya (Planner)",
    "NUTRITION": "Dr. Kai (Nutrition)",
    "DOCTOR": "Dr. Santos (Sports Medicine)",
}

VALID_ROUTES = frozenset(AGENT_PROMPTS)

_MEDICAL_ROUTE_PATTERN = re.compile(
    r"\b(pain|injury|injuries|soreness|swelling|sore|medical)\b",
    re.IGNORECASE,
)


def call_agent(system_prompt: str, user_message: str) -> str:
    api_key = "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"
    if not api_key:
        raise ValueError("Set GROQ_API_KEY in your environment.")

    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
    )
    content = completion.choices[0].message.content
    return content if content is not None else ""


def _parse_orchestrator_agent_list(raw: str) -> list[str]:
    first_line = raw.strip().split("\n")[0]
    parts = re.split(r"[,;]", first_line)
    out: list[str] = []
    for p in parts:
        token = p.strip().upper().strip(".,!?;:\"'")
        if token in VALID_ROUTES:
            out.append(token)
    return out


def orchestrate_agents(user_message: str) -> list[str]:
    raw = call_agent(ORCHESTRATOR_PROMPT, user_message)
    agents = _parse_orchestrator_agent_list(raw)
    seen: set[str] = set()
    ordered: list[str] = []
    for a in agents:
        if a not in seen:
            seen.add(a)
            ordered.append(a)
    if _MEDICAL_ROUTE_PATTERN.search(user_message) and "DOCTOR" not in ordered:
        ordered.append("DOCTOR")
    if not ordered:
        ordered = ["TECHNIQUE"]
    return ordered


def run_agent_pipeline(user_message: str) -> tuple[list[str], str]:
    agents = orchestrate_agents(user_message)
    previous_output = ""
    specialist_outputs: list[tuple[str, str]] = []

    for name in agents:
        if previous_output:
            combined = (
                f"Student question:\n{user_message}\n\n"
                "Context from the prior specialist (build on or align with this):\n"
                f"{previous_output}"
            )
        else:
            combined = user_message
        out = call_agent(AGENT_PROMPTS[name], combined)
        specialist_outputs.append((name, out))
        previous_output = out

    blocks = []
    for i, (_, text) in enumerate(specialist_outputs, 1):
        blocks.append(f"--- Contribution {i} ---\n{text}")
    synthesis_input = (
        f"Student question:\n{user_message}\n\n"
        "Specialist contributions to merge into one response:\n\n"
        + "\n\n".join(blocks)
    )
    final = call_agent(SYNTHESIZER_PROMPT, synthesis_input)
    return agents, final


if __name__ == "__main__":
    print("Martial arts coach — type your question (empty line or 'quit' to exit).\n")
    while True:
        try:
            user_message = input("You: ").strip()
        except EOFError:
            print()
            break
        if not user_message or user_message.lower() in ("quit", "exit", "q"):
            break

        agents, reply = run_agent_pipeline(user_message)
        labels = [AGENT_LABELS.get(a, a) for a in agents]
        print(f"\nOrchestrator: {', '.join(agents)}")
        print(f"Pipeline: {' → '.join(labels)}\n")
        print(reply)
        print()
