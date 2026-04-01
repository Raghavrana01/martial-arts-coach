"""
CrewAI martial arts coaching crew backed by Gemini (Gemini 2.5 Flash).

Five specialist agents run in sequence, then a Synthesizer merges their outputs.
Requires: crewai, python-dotenv, litellm.
"""

from __future__ import annotations

import asyncio
import sys
import time
from collections.abc import Callable
from pathlib import Path
from typing import Any, TypeVar

import os

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TRACING"] = "true"

from crewai import Agent, Crew, LLM, Process, Task
from crewai.tasks.task_output import TaskOutput
from dotenv import load_dotenv
from knowledge_base import search_knowledge

load_dotenv(Path(__file__).resolve().parent / ".env")
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY", "")

GEMINI_MODEL = "gemini/gemini-2.5-flash"

T = TypeVar("T")


def _format_conversation_history(
    conversation_history: list[dict[str, str]] | None,
) -> str:
    if not conversation_history:
        return "No prior conversation."

    lines: list[str] = []
    for message in conversation_history:
        role = message.get("role", "user").strip() or "user"
        content = message.get("content", "").strip()
        if not content:
            continue
        lines.append(f"{role.title()}: {content}")

    return "\n".join(lines) if lines else "No prior conversation."


def _is_rate_limit_error(exc: BaseException) -> bool:
    if getattr(exc, "status_code", None) == 429:
        return True
    name = type(exc).__name__
    if "RateLimit" in name or "TooManyRequests" in name:
        return True
    text = str(exc).lower()
    return (
        "429" in text
        or "rate limit" in text
        or "too many requests" in text
        or "resource exhausted" in text
    )


def call_agent(llm_call: Callable[..., T], *args: Any, **kwargs: Any) -> T:
    """Run *llm_call* (typically ``LLM.call``). On rate limit, wait 20s and retry once."""
    try:
        return llm_call(*args, **kwargs)
    except Exception as exc:
        if not _is_rate_limit_error(exc):
            raise
        time.sleep(20)
        return llm_call(*args, **kwargs)


async def _acall_agent(llm_acall: Callable[..., Any], *args: Any, **kwargs: Any) -> Any:
    """Async LLM path: same retry policy using ``asyncio.sleep``."""
    try:
        return await llm_acall(*args, **kwargs)
    except Exception as exc:
        if not _is_rate_limit_error(exc):
            raise
        await asyncio.sleep(20)
        return await llm_acall(*args, **kwargs)


def _patch_llm_retries(llm: LLM) -> None:
    """Wrap sync/async LLM entry points so rate limits trigger one retry after 20s."""
    orig_call = llm.call
    orig_acall = llm.acall

    def wrapped_call(*args: Any, **kwargs: Any) -> Any:
        return call_agent(orig_call, *args, **kwargs)

    async def wrapped_acall(*args: Any, **kwargs: Any) -> Any:
        return await _acall_agent(orig_acall, *args, **kwargs)

    llm.call = wrapped_call  # type: ignore[method-assign]
    llm.acall = wrapped_acall  # type: ignore[method-assign]


def _make_pause_between_tasks(num_tasks: int) -> Callable[[TaskOutput], None]:
    completed: list[int] = [0]

    def _pause_between_tasks(_output: TaskOutput) -> None:
        completed[0] += 1
        if completed[0] < num_tasks:
            time.sleep(3)

    return _pause_between_tasks


def _get_llm() -> LLM:
    llm = LLM(
        model=GEMINI_MODEL,
        temperature=0.4,
        api_key=os.environ.get("GEMINI_API_KEY"),
    )
    _patch_llm_retries(llm)
    return llm


def get_rag_context(query: str) -> str:
    """Retrieves relevant knowledge from the vector database."""
    results = search_knowledge(query, n_results=2)
    return "\n\n".join(results) if results else "No additional coaching manual context found."


def build_martial_arts_crew(user_message: str) -> tuple[Crew, str]:
    llm = _get_llm()
    rag_context = get_rag_context(user_message)

    technique_coach = Agent(
        role="Technique Coach",
        goal=(
            "Deliver expert, safety-conscious guidance on Muay Thai, Boxing, and Kickboxing "
            "strikes, combinations, footwork, guard, and biomechanics."
        ),
        backstory=(
            "You are a veteran striking coach who has trained amateur and pro fighters. "
            "You break down mechanics clearly, correct common mistakes, and always tie "
            "technique to balance, hip engagement, and protecting the chin."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    philosopher = Agent(
        role="Philosopher",
        goal=(
            "Strengthen the student's mindset, discipline, and motivation using Eastern "
            "wisdom, Stoicism, and Bruce Lee–style principles tied to their training."
        ),
        backstory=(
            "You are a calm, grounded mentor who connects daily training to larger life "
            "lessons. You speak with clarity and conviction about fear, consistency, "
            "ego, and the path of mastery."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    training_planner = Agent(
        role="Training Planner",
        goal=(
            "Design practical weekly training structures for combat sports athletes, "
            "with day-by-day ideas, duration, and intensity that fit the student's context."
        ),
        backstory=(
            "You are an elite strength and conditioning planner for boxers and nak muay. "
            "You balance skill work, sparring load, strength, and recovery so athletes "
            "peak without burning out."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    nutritionist = Agent(
        role="Nutritionist",
        goal=(
            "Give actionable fighter nutrition guidance: meals, snacks, hydration, weight "
            "management, recovery fuel, and sleep support using real foods."
        ),
        backstory=(
            "You are a sports dietitian who works with combat athletes making weight. "
            "You favor simple, affordable options and clear timing around training."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    doctor = Agent(
        role="Doctor",
        goal=(
            "Offer safety-first sports-medicine style guidance: possible concerns, "
            "first steps, load management, and when to seek in-person care—without "
            "claiming a definitive diagnosis."
        ),
        backstory=(
            "You are a sports medicine physician used to ringside and gym floor injuries. "
            "You prioritize red flags, conservative management, and clear escalation paths."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    synthesizer = Agent(
        role="Master Coach Coordinator",
        goal=(
            "Combine all specialist inputs into one concise, actionable response under 200 words."
        ),
        backstory=(
            "You have worked with all specialists and know how to distill their wisdom into "
            "clear guidance."
        ),
        llm=llm,
        verbose=False,
        allow_delegation=False,
    )

    technique_task = Task(
        description=(
            "Coach's memory of student:\n{user_memory}\n\n"
            "Recent conversation history:\n{conversation_history}\n\n"
            "Relevant knowledge from coaching manual:\n{rag_context}\n\n"
            "Student question:\n{student_question}\n\n"
            "Answer as the Technique Coach only. Focus on strikes, form, and training "
            "application for Muay Thai, Boxing, and/or Kickboxing as relevant. Be concise "
            "but specific."
        ),
        expected_output=(
            "Structured technical coaching: key cues, common errors, and 2–4 drills or "
            "progressions the student can use this week."
        ),
        agent=technique_coach,
    )

    philosophy_task = Task(
        description=(
            "Coach's memory of student:\n{user_memory}\n\n"
            "Recent conversation history:\n{conversation_history}\n\n"
            "Student question:\n{student_question}\n\n"
            "The Technique Coach has already responded (see context). Build on that output: "
            "add mindset, motivation, and philosophy (Stoicism, Eastern thought, Bruce Lee "
            "wisdom) that support the same training theme. Do not repeat the whole "
            "technique section—extend it mentally and emotionally."
        ),
        expected_output=(
            "A short, powerful mindset section: themes to remember, how to train with "
            "intention, and one or two reflective practices."
        ),
        agent=philosopher,
        context=[technique_task],
    )

    planner_task = Task(
        description=(
            "Coach's memory of student:\n{user_memory}\n\n"
            "Recent conversation history:\n{conversation_history}\n\n"
            "Student question:\n{student_question}\n\n"
            "The Philosopher's output is in context (along with prior work). Propose a "
            "one-week training outline that fits the student's implied level and goals. "
            "Use day-by-day bullets with duration and intensity (e.g. easy/moderate/hard)."
        ),
        expected_output=(
            "7-day plan (Mon–Sun or Day 1–7) with sessions, duration, and intensity; "
            "note one full rest or active recovery day if appropriate."
        ),
        agent=training_planner,
        context=[philosophy_task],
    )

    nutrition_task = Task(
        description=(
            "Coach's memory of student:\n{user_memory}\n\n"
            "Recent conversation history:\n{conversation_history}\n\n"
            "Student question:\n{student_question}\n\n"
            "Using the Training Planner's output in context, suggest nutrition and "
            "hydration that support that week: pre/post training meals, snacks, and "
            "sleep habits. Mention weight management only if the question implies it."
        ),
        expected_output=(
            "Practical meal and hydration ideas with timing; recovery nutrition; "
            "sleep tips—using concrete foods, not vague advice."
        ),
        agent=nutritionist,
        context=[planner_task],
    )

    doctor_task = Task(
        description=(
            "Coach's memory of student:\n{user_memory}\n\n"
            "Recent conversation history:\n{conversation_history}\n\n"
            "Student question:\n{student_question}\n\n"
            "Review the Nutritionist's output in context (and the chain before it). "
            "Add sports-medicine perspective: training safety, injury prevention or "
            "red flags if relevant, and when to see a real clinician. Never give a "
            "definitive diagnosis."
        ),
        expected_output=(
            "Safety-first wrap-up: what to monitor, conservative training rules if "
            "hurting, and clear 'see a doctor' triggers when appropriate."
        ),
        agent=doctor,
        context=[nutrition_task],
    )

    synthesizer_task = Task(
        description=(
            "Coach's memory of student:\n{user_memory}\n\n"
            "Recent conversation history:\n{conversation_history}\n\n"
            "Student question:\n{student_question}\n\n"
            "You have the full outputs from five specialists in context (technique, philosophy, "
            "training plan, nutrition, and sports-medicine safety). Merge them into ONE unified "
            "answer for the student. Speak as a single coach—do not name or label the specialists. "
            "Prioritize clarity and action steps. Hard limit: stay under 200 words."
        ),
        expected_output=(
            "One cohesive response under 200 words: what to do this week, how to think about it, "
            "and any safety notes if relevant."
        ),
        agent=synthesizer,
        context=[
            technique_task,
            philosophy_task,
            planner_task,
            nutrition_task,
            doctor_task,
        ],
    )


    return Crew(
        agents=[
            technique_coach,
            philosopher,
            training_planner,
            nutritionist,
            doctor,
            synthesizer,
        ],
        tasks=[
            technique_task,
            philosophy_task,
            planner_task,
            nutrition_task,
            doctor_task,
            synthesizer_task,
        ],
        process=Process.sequential,
        verbose=False,
        task_callback=_make_pause_between_tasks(6),
    ), rag_context


def run_agent_pipeline(
    user_message: str,
    conversation_history: list[dict[str, str]] | None = None,
    user_memory: str | None = None,
) -> tuple[list[str], str]:
    """Run the CrewAI crew and return (agent roles in order, final synthesized reply)."""
    crew, rag_context = build_martial_arts_crew(user_message)
    result = crew.kickoff(
        inputs={
            "student_question": user_message,
            "conversation_history": _format_conversation_history(conversation_history),
            "user_memory": user_memory or "No prior memory.",
            "rag_context": rag_context,
        }
    )

    activated: list[str] = []
    if result.tasks_output:
        activated = [t.agent for t in result.tasks_output]

    final_text = ""
    if result.tasks_output:
        final_text = result.tasks_output[-1].raw
    if not final_text.strip():
        final_text = result.raw if result.raw else str(result)

    return activated, final_text.strip()


def main() -> None:
    if not os.environ.get("GEMINI_API_KEY"):
        print(
            "Missing GEMINI_API_KEY. Add it to your .env file next to crew_coach.py.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        user_line = input("You: ").strip()
    except EOFError:
        user_line = ""

    if not user_line:
        return

    student_question = user_line

    _agents, final_text = run_agent_pipeline(student_question)

    print(final_text)


if __name__ == "__main__":
    main()
