import requests
from typing import List, Dict
from rag.vector_store import query_vector_store
from rag.utils import get_logger
import time

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.1:8b"
chat_history = []

def query_ollama(prompt: str, log_raw: bool = False) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }
    try:
        response = requests.post(OLLAMA_URL, json=payload)
        response.raise_for_status()
        data = response.json()
        if log_raw:
            logger = get_logger("ollama_raw", "ollama_raw.log")
            logger.info(data)
        return data["response"]
    except Exception as e:
        return f"[Error contacting Ollama: {str(e)}]"

def build_prompt(query: str, retrieved_chunks: List[Dict], history: List[Dict]) -> str:
    context = "\n\n".join([chunk["text"] for chunk in retrieved_chunks])
    history_text = "\n".join([f"User: {h['user']}\nBot: {h['bot']}" for h in history])
    
    # --- START of MODIFICATION ---
    persona_instruction = (
        f"You are an AI assistant specialized in firewall administration documentation. "
        f"Your goal is to provide clear, concise, and accurate information based *only* on the provided context. "
        f"If the information is not in the context, state that you cannot answer based on the available documentation.\n\n"
    )
    # --- END of MODIFICATION ---

    prompt = (
        persona_instruction + # Concatenate the new persona instruction
        f"Context from documents:\n{context}\n\n"
        f"Conversation so far:\n{history_text}\n\n"
        f"User question: {query}\n\n"
        f"Answer:"
    )
    return prompt

def handle_chat(user_input: str, log_chunks=False, log_prompt=False, log_latency=False, log_raw=False) -> str:
    retrieved = query_vector_store(user_input)
    if log_chunks:
        logger = get_logger("retrieved_chunks", "retrieved_chunks.log")
        for i, chunk in enumerate(retrieved):
            logger.info(f"Chunk {i}: {chunk['text'][:100]}")

    prompt = build_prompt(user_input, retrieved, chat_history)

    if log_prompt:
        logger = get_logger("prompt", "prompt.log")
        logger.info(prompt)

    start = time.time()
    response = query_ollama(prompt, log_raw=log_raw)
    latency = time.time() - start

    if log_latency:
        logger = get_logger("latency", "latency.log")
        logger.info(f"LLM response time: {latency:.2f}s")

    chat_history.append({"user": user_input, "bot": response})
    return response

def reset_chat_memory():
    global chat_history
    chat_history = []