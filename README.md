# Mini RAG – Retrieval Augmented Generation App

A simple Retrieval-Augmented Generation (RAG) web application.  
Users can ingest text to build a small knowledge base and then ask questions. The system retrieves relevant chunks from a vector database and generates grounded answers with inline citations.

This project demonstrates a practical RAG pipeline with embeddings, vector search, and an LLM, packaged as a small, deployable web app.

* * *

## Features

-   Ingest plain text into a vector database
    
-   Chunking + embeddings for semantic search
    
-   Retrieve relevant context for a question
    
-   LLM-generated answers with citations like `[1]`, `[2]`
    
-   Split-screen web UI (ingestion + Q&A)
    
-   Clean REST API with FastAPI
    

* * *

## Tech Stack

-   **Backend:** FastAPI (Python)
    
-   **Embeddings:** Voyage AI
    
-   **Vector Database:** Supabase (pgvector)
    
-   **LLM:** Groq
    
-   **Frontend:** HTML, CSS, JavaScript
    

* * *

## Architecture (High Level)

    Browser UI
       |
       v
    FastAPI Backend
       |
       |-- Embeddings (Voyage)
       |-- Vector Search (Supabase pgvector)
       |-- LLM (Groq)
       |
    Answer + Citations
    

* * *

## Project Structure

    mini-rag/
      ├── backend/
      │   ├── main.py
      │   ├── rag.py
      │   ├── db.py
      │   ├── requirements.txt
      │   └── .env
      └── frontend/
          └── index.html
    

* * *

## Prerequisites

-   Python 3.10+
    
-   Supabase account (with pgvector enabled)
    
-   Voyage AI API key
    
-   Groq API key
    

* * *

## Setup

### 1\. Clone the repository

    git clone <your-repo-url>
    cd mini-rag/backend
    

* * *

### 2\. Create and activate a virtual environment

**Windows (PowerShell):**

    python -m venv venv
    .\venv\Scripts\Activate.ps1
    

**macOS / Linux:**

    python3 -m venv venv
    source venv/bin/activate
    

* * *

### 3\. Install dependencies

    pip install -r requirements.txt
    

* * *

### 4\. Configure environment variables

Create a `.env` file inside `backend/`:

    SUPABASE_URL=your_supabase_project_url
    SUPABASE_KEY=your_supabase_anon_key
    VOYAGE_API_KEY=your_voyage_api_key
    GROQ_API_KEY=your_groq_api_key
    

* * *

### 5\. Supabase setup (Vector Database)

Run the following SQL in the Supabase SQL Editor:

    create extension if not exists vector;
    
    drop table if exists documents;
    
    create table documents (
      id uuid primary key default gen_random_uuid(),
      content text,
      embedding vector(1024)
    );
    
    create or replace function match_documents(
      query_embedding vector(1024),
      match_count int
    )
    returns table (content text)
    language sql stable as $$
      select content
      from documents
      order by embedding <-> query_embedding
      limit match_count;
    $$;
    
    alter table documents disable row level security;
    

* * *

### 6\. Run the backend

    uvicorn main:app --reload
    

The API will be available at:

    http://127.0.0.1:8000
    

* * *

### 7\. Run the frontend

Open `frontend/index.html` in your browser  
(or serve it using a local server like VS Code Live Server).

Ensure the backend is running before using the UI.

* * *

## API Endpoints

### POST `/ingest`

Ingest text into the vector database.

**Request:**

    { "text": "Your content here" }
    

**Response:**

    { "status": "ingested" }
    

* * *

### POST `/query`

Query the knowledge base using RAG.

**Request:**

    { "question": "Your question here" }
    

**Response:**

    {
      "answer": "Generated answer with citations [1] [2].",
      "sources": [
        { "content": "Source text 1" },
        { "content": "Source text 2" }
      ]
    }
    

* * *

## How to Use

1.  Paste text into the ingestion panel and click **Ingest**
    
2.  Ask a question in the Q&A panel
    
3.  View the answer with inline citations and source content
    

* * *

## Example

**Input text:**

    Voyage AI provides high quality embedding models for semantic search and RAG applications.
    

**Question:**

    What is Voyage AI used for?
    

**Output:**

    Answer: Voyage AI is used for providing embedding models for semantic search and RAG applications [1].
    
    [1] Voyage AI provides high quality embedding models for semantic search and RAG applications.
    

* * *

## Common Issues

-   **CORS errors in browser**  
    Ensure CORS middleware is enabled in `main.py`.
    
-   **No results found**  
    Make sure you ingest text before querying.
    
-   **Supabase insert errors**  
    Ensure Row Level Security (RLS) is disabled for the `documents` table during development.
    
-   **Rate limits / quota errors**  
    Free-tier API limits may block requests. Check provider dashboards.
    

* * *

## Limitations

-   Text-only ingestion (no file uploads yet)
    
-   No authentication or multi-user support
    
-   Basic retrieval without reranking
    

* * *

## Future Improvements

-   File uploads (PDF, TXT)
    
-   Reranking (MMR or cross-encoders)
    
-   Streaming responses from the LLM
    
-   Better source deduplication
    
-   User authentication and history
    

* * *

## License

This project is for learning and demonstration purposes. 

