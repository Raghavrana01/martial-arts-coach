from martial_arts_knowledge import KNOWLEDGE_DOCUMENTS
from knowledge_base import build_knowledge_base, knowledge_base_exists

def setup():
    """Initializes the RAG knowledge base if it doesn't already exist."""
    if knowledge_base_exists():
        print("Knowledge base already exists. Skipping initialization.")
        return

    print("Knowledge base not found. Initializing with coaching documents...")
    try:
        build_knowledge_base(KNOWLEDGE_DOCUMENTS)
        print(f"Knowledge base built successfully with {len(KNOWLEDGE_DOCUMENTS)} documents.")
    except Exception as e:
        print(f"Error during knowledge base setup: {e}")

if __name__ == "__main__":
    setup()
