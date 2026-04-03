import json
import os
from pathlib import Path
from dotenv import load_dotenv
import litellm

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["CREWAI_DISABLE_TRACING"] = "true"

# Load environment variables from .env file
load_dotenv(Path(__file__).resolve().parent / ".env")
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY", "")

MODEL = "gemini/gemini-2.5-flash"

def get_memory_file(username: str) -> Path:
    """Returns the Path to the user-specific memory file."""
    return Path(__file__).resolve().parent / f"memory_{username}.json"

def save_memory(facts: dict, username: str):
    """Saves the provided facts dictionary to memory_{username}.json."""
    memory_file = get_memory_file(username)
    with open(memory_file, "w", encoding="utf-8") as f:
        json.dump(facts, f, indent=4, ensure_ascii=False)

def load_memory(username: str) -> dict:
    """Loads and returns the facts dictionary from memory_{username}.json, returns empty dict if not found."""
    memory_file = get_memory_file(username)
    if not memory_file.exists():
        return {}
    try:
        with open(memory_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}

def extract_facts(conversation_history: list, username: str) -> dict:
    """
    Calls Gemini API via litellm to extract key facts (experience, goals, injuries, techniques)
    from the conversation history and returns them as a dictionary.
    The username is used for logging/tracking purposes.
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Set GEMINI_API_KEY in .env or your environment.")

    # Format conversation history for the extraction prompt
    history_str = ""
    for msg in conversation_history:
        role = msg.get("role", "user").title()
        content = msg.get("content", "")
        history_str += f"{role}: {content}\n"

    system_prompt = (
        "You are an expert at extracting structured information from conversations. "
        "Extract key facts about the martial arts student from the provided chat history. "
        "Focus on: training experience, goals, injuries, and techniques practiced. "
        "Return ONLY a valid JSON object with these categories as keys. "
        "If no information is found for a category, use an empty string or empty list. "
        "Do not include any explanation or other text."
    )

    try:
        response = litellm.completion(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Extract facts from this history:\n\n{history_str}"},
            ],
            api_key=api_key,
            response_format={"type": "json_object"},
        )
        content = response.choices[0].message.content
        if content:
            return json.loads(content)
        return {}
    except Exception as e:
        print(f"Error extracting facts via litellm: {e}")
        return {}

if __name__ == "__main__":
    # Quick self-test logic (optional)
    test_history = [
        {"role": "user", "content": "I've been training Muay Thai for 2 years but my shins always hurt after heavy bag work. I want to improve my head kicks."},
    ]
    print("Extracting facts for test...")
    # This will only work if GEMINI_API_KEY is set in .env
    # facts = extract_facts(test_history, "test_user")
    # print(facts)
