import os
from pathlib import Path
import chromadb
from chromadb.utils import embedding_functions

# Configuration
DB_PATH = str(Path(__file__).resolve().parent / "chroma_db")
COLLECTION_NAME = "martial_arts_knowledge"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Use sentence-transformers embedding function
embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)

def _get_client():
    """Returns a persistent ChromaDB client."""
    return chromadb.PersistentClient(path=DB_PATH)

def build_knowledge_base(documents: list[str]):
    """
    Takes a list of text documents, generates embeddings, 
    and stores them in the ChromaDB collection.
    """
    client = _get_client()
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=embedding_func
    )
    
    # Generate unique IDs for the documents
    ids = [f"doc_{i}" for i in range(len(documents))]
    
    # Upsert documents into the collection
    collection.upsert(
        documents=documents,
        ids=ids
    )
    print(f"Successfully added {len(documents)} documents to knowledge base.")

def search_knowledge(query: str, n_results: int = 3) -> list[str]:
    """
    Searches the knowledge base for the most relevant chunks 
    matching the query.
    """
    client = _get_client()
    try:
        collection = client.get_collection(
            name=COLLECTION_NAME,
            embedding_function=embedding_func
        )
        
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Flatten the nested list of results returned by Chroma
        return results['documents'][0] if results['documents'] else []
    except Exception as e:
        print(f"Knowledge base search error: {e}")
        return []

def knowledge_base_exists() -> bool:
    """
    Returns True if the chroma_db folder exists and contains 
    the expected collection data.
    """
    db_folder = Path(DB_PATH)
    if not db_folder.exists():
        return False
        
    client = _get_client()
    try:
        # Check if the collection exists and has documents
        collection = client.get_collection(name=COLLECTION_NAME)
        return collection.count() > 0
    except Exception:
        return False

if __name__ == "__main__":
    # Self-test logic
    if not knowledge_base_exists():
        print("Knowledge base not found. Building a sample...")
        sample_docs = [
            "The roundhouse kick is a powerful strike in Muay Thai, emphasizing hip rotation and hitting with the shin.",
            "Stance and guard are the foundation of defensive boxing. Keep your chin down and hands high.",
            "Muay Thai clinch work involves controlling the opponent's head and neck to deliver knee strikes."
        ]
        build_knowledge_base(sample_docs)
    
    print("Searching knowledge base for 'roundhouse kick'...")
    results = search_knowledge("roundhouse kick")
    for i, res in enumerate(results, 1):
        print(f"Result {i}: {res}")
