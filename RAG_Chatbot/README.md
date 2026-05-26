# RAG Chatbot with Conversation History

A local Retrieval-Augmented Generation (RAG) pipeline that lets you chat with your documents using open-source models via Ollama.

---

## Architecture

```
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

## How It Works

### 1. Ingestion (`ingestion_pipeline.py`)
- Loads all `.txt` files from the `docs/` folder
- Splits them into chunks (`1000 chars`, `100 overlap`)
- Embeds each chunk using `bge-m3` via Ollama
- Stores vectors in ChromaDB at `db/chroma_db`

### 2. Retrieval (`retrieval_pipeline.py`)
- Loads the persisted ChromaDB store
- Runs similarity search with a score threshold (`≥ 0.3`)
- Returns the top-K relevant chunks for a query

### 3. Generation with History (`history_aware_generation.py`)
- Rewrites the user question into a standalone search query using chat history
- Retrieves top-3 relevant chunks
- Feeds chunks + history into the LLM for a grounded answer
- Stores each Q&A turn in `chat_history` for multi-turn context

---

## Models Used

| Role        | Model              | Provider |
|-------------|--------------------|----------|
| Embeddings  | `bge-m3`           | Ollama   |
| Chat / LLM  | `llama3.2:3b`      | Ollama   |

> All models run **locally** — no API keys needed.

---

## Project Structure

```
project/
├── docs/                        # Put your .txt documents here
├── db/
│   └── chroma_db/               # Auto-created vector store
├── ingestion_pipeline.py        # Step 1: ingest & embed docs
├── retrieval_pipeline.py        # Step 2: test retrieval
├── history_aware_generation.py  # Step 3: chat with history
└── .env                         # Environment variables
```

---

## Quick Start

**1. Install dependencies**
```bash
pip install langchain langchain-chroma langchain-ollama langchain-openai python-dotenv
```

**2. Pull models via Ollama**
```bash
ollama pull bge-m3
ollama pull llama3.2:3b
```

**3. Add your documents**
```bash
mkdir docs
# copy your .txt files into docs/
```

**4. Ingest documents**
```bash
python ingestion_pipeline.py
```

**5. Start chatting**
```bash
python history_aware_generation.py
```

---

## Vector Store

- **Engine:** ChromaDB (local, persistent)
- **Distance metric:** Cosine similarity
- **Chunk size:** 1000 characters | **Overlap:** 100 characters
- **Retrieval:** Top-K with optional score threshold (`≥ 0.3`)