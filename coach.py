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

ROUTING_SYSTEM_PROMPT = (
    "You are a routing classifier. Read the user's message and reply with exactly one "
    "word, with no punctuation or explanation:\n"
    "- TECHNIQUE — how to execute strikes, footwork, guard, drills, pad work, form, technique\n"
    "- PHILOSOPHY — mindset, discipline, fear, motivation, life lessons, wisdom, mental game\n"
    "- PLANNER — weekly schedule, training plan, periodization, conditioning structure, programming\n"
    "- NUTRITION — meals, diet, weight cut, hydration, supplements, sleep, recovery food\n"
    "Do not reply with DOCTOR; medical topics are routed separately."
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


def _normalize_route(raw: str) -> str:
    first = raw.strip().split()[0].upper().strip(".,!?;:\"'")
    return first if first in VALID_ROUTES else "TECHNIQUE"


def route_message(user_message: str) -> str:
    if _MEDICAL_ROUTE_PATTERN.search(user_message):
        return "DOCTOR"
    raw = call_agent(ROUTING_SYSTEM_PROMPT, user_message)
    return _normalize_route(raw)


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

        route = route_message(user_message)
        label = AGENT_LABELS.get(route, route)
        print(f"\n[{route}] {label} is responding...\n")
        reply = call_agent(AGENT_PROMPTS[route], user_message)
        print(reply)
        print()
