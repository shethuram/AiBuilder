# RAG Chatbot with Conversation History

A simple local Retrieval-Augmented Generation (RAG) chatbot built using LangChain, ChromaDB, Ollama, and Streamlit.

The project allows users to chat with their own documents using open-source local LLMs with conversation history support.

---

# Architecture

```text
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Your Docs  │────▶│ Ingestion Pipeline│────▶│  ChromaDB Store │
│  (.txt)     │     │ (chunk + embed)   │     │  (persisted)    │
└─────────────┘     └──────────────────┘     └────────┬────────┘
                                                       │
                                                       │ vector search
                                                       ▼
┌─────────────┐     ┌──────────────────┐     ┌─────────────────┐
│    Answer   │◀────│   LLM (Ollama)   │◀────│ Top-K Chunks    │
│             │     │  llama3.2:3b     │     │ (retrieved)     │
└─────────────┘     └──────────────────┘     └─────────────────┘
       ▲                    ▲
       │                    │
       └────────────────────┘
            chat_history
         (multi-turn context)
```

---

# Features

* Local RAG pipeline using Ollama
* Conversation-aware question answering
* ChromaDB persistent vector storage
* Context-aware retrieval
* Streamlit chat interface
* Source + Chunk ID citations
* No API keys required

---

# How It Works

## 1. Ingestion (`ingestion_pipeline.py`)

* Loads `.txt` documents from the `docs/` folder
* Splits documents into chunks
* Generates embeddings using `bge-m3`
* Stores embeddings in ChromaDB

## 2. Retrieval (`retrieval_pipeline.py`)

* Loads persisted vector database
* Performs similarity search
* Retrieves top relevant chunks

## 3. Generation (`history_aware_generation.py`)

* Uses conversation history to rewrite queries
* Retrieves relevant chunks
* Sends chunks + history to the LLM
* Generates grounded answers with citations

## 4. Streamlit UI (`streamlit_app.py`)

* Simple chatbot interface
* Maintains session chat history
* Displays user and assistant messages interactively

---

# Models Used

| Role       | Model         | Provider |
| ---------- | ------------- | -------- |
| Embeddings | `bge-m3`      | Ollama   |
| LLM        | `llama3.2:3b` | Ollama   |

> All models run locally.

---

# Project Structure

```text
project/
├── docs/                        
├── db/
│   └── chroma_db/
├── ingestion_pipeline.py
├── retrieval_pipeline.py
├── history_aware_generation.py
├── streamlit_app.py
├── .env
└── README.md
```

---

# Installation

## 1. Create Virtual Environment

```bash
python -m venv venv
```

## 2. Activate Environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install streamlit langchain langchain-community langchain-chroma langchain-ollama langchain-openai chromadb python-dotenv
```

---

# Pull Ollama Models

```bash
ollama pull bge-m3
ollama pull llama3.2:3b
```

---

# Add Documents

Create a `docs/` folder and place your `.txt` files inside it.

```bash
mkdir docs
```

---

# Run Ingestion Pipeline

```bash
python ingestion_pipeline.py
```

This creates the ChromaDB vector store inside:

```text
db/chroma_db
```

---

# Start Streamlit Chatbot

```bash
streamlit run streamlit_app.py
```

---

# Vector Store Details

* Vector DB: ChromaDB
* Embedding Model: `bge-m3`
* Similarity Metric: Cosine Similarity
* Chunk Size: 1000
* Chunk Overlap: 100
* Retrieval: Top-K Similarity Search

---

# Example Workflow

1. Add documents to `docs/`
2. Run ingestion pipeline
3. Launch Streamlit app
4. Ask questions about your documents
5. Receive grounded answers with citations

---

# Tech Stack

* Python
* LangChain
* ChromaDB
* Ollama
* Streamlit

---

## Output

Refer [Simple RAG Chat Output](output/Simple_RAG_Chat.pdf) for the output.
