 # RAGworks Retrieval-Augmented Generation (RAG) system.
## This document is intended for developers who want to understand, modify, or extend the Retrieval-Augmented Generation (RAG) system.
## This application allows users to upload documents and ask questions.
## The system retrieves relevant content from stored documents and uses an LLM to generate grounded responses.


# Architecture 
Frontend: React 
Backend: Flask (API Layer)
Vector Database: ChromaDB (Stores embeddings)
Relational Database: MYSQL (Stores metadata and logs)
LLM + Embeddings + Evaluation: OpenAI API

User → React Frontend → Flask API → ChromaDB → OpenAI API → Flask → React → User

# Key Components (files)
BACKEND
app.py (Flask Backend)
    Defines API routes: 
        * /query - handles user questions 
        * /upload - uploads documents to the system
        * /admin → admin-level operations 
    Connects the frontend requests to the backend logic 

rag_logic.py (Core RAG System Logic)
    * Document ingestion
    * Text chunking
    * Embedding generation
    * Vector storage (ChromaDB)
    * Retrieval (top_k search)
    * Response generation using LLM
FRONTEND 
App.js (Main Entry)
    * root component of the React application 
    * Handles routing between user and admin views

    Query Handling 
    * captures user input 

# Document Ingestion Pipeline 
When a document is uploaded:
    1. File is parsed (supports PDF, DOCX, TXT, HTML, etc.)
    2. Text is split into chunks
    3. Each chunk is converted into an embedding using OpenAI 
    4. Embeddins are stored in Chroma DB with metadata
        * source file name 
        * upload timestamp 
        * unique ID 

# Retrieval + Generation
When answering a query:
    * Query is embedded
    * Top k relevant chunks are retrieved
    * Context is passed into the LLM
    * Response is generated based only on retrieved context
Key Parameters:
    * top_k → number of chunks retrieved
    * temperature → randomness of response
    * top_p → vocabulary diversity

# Evaluation System
eval_questions.py (evaluates the accuracy of the system)

Metrics: 
    * Answer accuracy 
    * Source accuracy 

Parameters tested: 
    * top_k = 3, 5, 8
    * temperature = 0.0 – 0.2
    * top_p = 0.8 – 1.0

Final Insight: Increasing top_k improved both answer and source accuracy by providing more context to the model. There is a limit to this performance. Performance does not increase linear to k. 

IMPORTANT
Update json evaluation file name for new results or risk replacing the old on future runs. 


# Environment Setup 
Sensitive information stored in .env 
    * OpenAI API key 
    * MySQL credentials

# Important Notes 
ChromaDB is stored locally in chroma_storage/ 
    Avoid committing: 
    * .env 
    * chroma_storage/
    * _pycache_/
    * vector database files 
    Update gitignore for future sensitive files
MySQL must be running locally for storage functionality

# Live application 
Please see SETUP.md for instructions on properly running the RAG system. 
