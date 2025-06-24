# Simple RAG Chat Application (Local with Ollama)

This project provides a beginner-friendly Retrieval Augmented Generation (RAG) chat application that runs entirely locally, leveraging Ollama for both the Large Language Model (LLM) and embedding models. It allows you to chat with your own PDF and DOCX documents.

## Features

* **Local Execution:** Everything runs on your machine using Ollama, ensuring privacy and no external API costs.
* **Document Ingestion:** Upload PDF and DOCX files. [cite: app.py, loader.py]
* **Text Chunking:** Documents are automatically broken down into manageable chunks. [cite: loader.py, chunker.py]
* **Vector Store:** Uses ChromaDB as a local vector database for efficient semantic search of document chunks. [cite: vector_store.py]
* **Contextual Chat:** The LLM answers questions using context retrieved from your uploaded documents. [cite: chat_engine.py]
* **Chat History:** Maintains conversation history for more coherent interactions. [cite: chat_engine.py, memory.py]
* **Streamlit UI:** A simple and intuitive web interface for uploading documents and chatting. [cite: app.py]
* **Debugging Options:** Toggle logging for retrieved chunks, LLM prompts, latency, vector store operations, and raw Ollama responses. [cite: app.py, chat_engine.py, vector_store.py, utils.py]

## Prerequisites

Before running the application, ensure you have the following installed:

1.  **Python 3.8+**: Download from [python.org](https://www.python.org/).
2.  **Git**: For cloning the repository.
3.  **Ollama**:
    * Download and install Ollama from [ollama.ai](https://ollama.ai/).
    * After installation, open your terminal or command prompt and pull the necessary models:
        ```bash
        ollama pull llama2 # For the Large Language Model
        ollama pull nomic-embed-text # For generating document embeddings
        ```
    * Ensure Ollama is running in the background.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repo-name.git](https://github.com/your-username/your-repo-name.git) # Replace with actual repo URL
    cd your-repo-name
    ```
2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set Environment Variables (Optional but Recommended):**
    Create a `.env` file in the root directory of the project and add the following (these are the defaults, change if your Ollama server or model names are different):
    ```
    LLM_SERVER=http://localhost:11434
    EMBED_MODEL=nomic-embed-text
    MODEL_NAME=llama2
    ```

## How to Run

1.  Ensure Ollama is running and you have pulled `llama2` and `nomic-embed-text` models.
2.  From the project's root directory, run the Streamlit application:
    ```bash
    streamlit run app.py
    ```
3.  Your web browser will automatically open the RAG Chat Application.

## Usage

1.  **Upload Documents:**
    * In the sidebar, use the "Upload Document" section to choose PDF or DOCX files. [cite: app.py]
    * Once uploaded, the document will appear in the "Uploaded Documents" list. The application automatically processes and adds its content to the vector store. [cite: app.py]
2.  **Delete Documents:**
    * You can remove uploaded documents from the list by clicking the "❌ Delete" button next to their name. This also removes their corresponding vectors from the ChromaDB. [cite: app.py, vector_store.py]
3.  **Chat Interface:**
    * Type your questions in the "Ask a question about your documents:" text box.
    * Click "Send" to get a response from the RAG assistant. [cite: app.py]
4.  **Reset Chat:**
    * Click "Reset Chat" to clear the conversation history. [cite: app.py, chat_engine.py, memory.py]
5.  **Debug Options (Sidebar):**
    * Enable various checkboxes in the "Debug Options" section in the sidebar to log internal processes to files in the `logs/` directory. [cite: app.py]

## Project Structure

* `app.py`: The main Streamlit application script. Handles UI and orchestrates RAG flow. [cite: app.py]
* `rag/`:
    * `chat_engine.py`: Manages the interaction with the LLM, prompt building, and integrating retrieved context. [cite: chat_engine.py]
    * `chunker.py`: Contains a simple text chunking utility. [cite: chunker.py]
    * `loader.py`: Handles loading and extracting text from PDF and DOCX files, and initial chunking. [cite: loader.py]
    * `memory.py`: Defines a simple class for managing chat history. [cite: memory.py]
    * `vector_store.py`: Manages interactions with ChromaDB (adding, deleting, querying vectors) and remote embedding via Ollama. [cite: vector_store.py]
    * `utils.py`: Provides logging utilities for the application. [cite: utils.py]
* `cache/uploaded_files/`: Directory where uploaded documents are temporarily stored. [cite: app.py]
* `chroma_data/`: Directory where ChromaDB persists its vector store data. [cite: vector_store.py]
* `logs/`: Directory where various application logs are stored. [cite: utils.py]
* `.env`: (Optional) File to store environment variables like Ollama server URL and model names.
* `requirements.txt`: Lists all Python dependencies required for the project.

---