# rag/vector_store.py
from dotenv import load_dotenv
load_dotenv()
# Removed 'from chromadb.config import Settings' as it's often not needed for PersistentClient directly
from chromadb import PersistentClient # Import PersistentClient instead of Client
from typing import List, Dict
import requests
from rag.utils import get_logger
import os

# Remote embedding model via Ollama
LLM_SERVER = os.getenv("LLM_SERVER", "http://localhost:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

# Local ChromaDB setup - Updated client instantiation
# Use PersistentClient for a persistent DuckDB-backed ChromaDB
chroma_client = PersistentClient(path="./chroma_data") # Specify the persist directory here

collection = chroma_client.get_or_create_collection(name="rag_docs")

def remote_embed(texts: List[str]) -> List[List[float]]:
    embeddings = []
    for text in texts:
        response = requests.post(f"{LLM_SERVER}/api/embeddings", json={"model": EMBED_MODEL, "prompt": text})
        response.raise_for_status()
        embeddings.append(response.json()["embedding"])
    return embeddings

def add_to_vector_store(doc_id: str, chunks: List[Dict], log=False):
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    embeddings = remote_embed(texts)

    collection.add(documents=texts, metadatas=metadatas, ids=ids, embeddings=embeddings)

    if log:
        logger = get_logger("vector_store", "vector_store.log")
        logger.info(f"Added {len(chunks)} chunks from {doc_id} to local ChromaDB.")

def remove_from_vector_store(doc_id: str, log=False):
    result = collection.get()
    ids_to_remove = [id for id, meta in zip(result["ids"], result["metadatas"]) if meta["source"] == doc_id]
    if ids_to_remove:
        collection.delete(ids=ids_to_remove)
        if log:
            logger = get_logger("vector_store", "vector_store.log")
            logger.info(f"Removed {len(ids_to_remove)} vectors for {doc_id} from ChromaDB.")

def query_vector_store(query: str, k: int = 5) -> List[Dict]:
    embedding = remote_embed([query])[0]
    results = collection.query(query_embeddings=[embedding], n_results=k)
    return [
        {"text": doc, "metadata": meta}
        for doc, meta in zip(results['documents'][0], results['metadatas'][0])
    ]