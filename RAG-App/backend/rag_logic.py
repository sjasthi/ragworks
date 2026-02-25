# backend/rag_logic.py
import os
from openai import OpenAI, AuthenticationError
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from docx import Document
import chromadb
from chromadb.utils import embedding_functions

# Load environment variables
load_dotenv()

# OpenAI Client
def create_client(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        return client
    except AuthenticationError:
        print("Invalid API key.")
        return None

# Load API key from .env or ask
api_key = os.environ.get("OPENAI_KEY")
if not api_key:
    api_key = input("Enter your OpenAI API key: ").strip()

client = create_client(api_key)

# Persistent Chroma Setup
persist_dir = os.path.abspath("chroma_storage")
chroma_client = chromadb.PersistentClient(path=persist_dir)

embedding_function = embedding_functions.OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small"
)

database = chroma_client.get_or_create_collection(
    name="RAG_Work_test",
    embedding_function=embedding_function
)

# --- Helper Functions ---

def normalize_path(path):
    return os.path.abspath(path)

def file_already_exists(file_path):
    file_path = normalize_path(file_path)
    results = database.get(where={"source": file_path}, limit=1)
    return len(results["ids"]) > 0

def chunk_text(text, chunk_size=800, overlap=150):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

# --- File ingestion ---
def add_html(file_path):
    file_path = normalize_path(file_path)
    if file_already_exists(file_path):
        return "File already uploaded."
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    soup = BeautifulSoup(content, "html.parser")
    text = soup.get_text(separator=" ", strip=True)
    chunks = chunk_text(text)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    database.add(
        documents=chunks,
        ids=[f"{file_name}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file_path} for _ in chunks]
    )
    return f"Added successfully. Collection size: {database.count()}"

def add_docx(file_path):
    file_path = normalize_path(file_path)
    if file_already_exists(file_path):
        return "File already uploaded."
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    chunks = chunk_text(text)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    database.add(
        documents=chunks,
        ids=[f"{file_name}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file_path} for _ in chunks]
    )
    return f"Added successfully. Collection size: {database.count()}"

def add_txt(file_path):
    file_path = normalize_path(file_path)
    if file_already_exists(file_path):
        return "File already uploaded."
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    database.add(
        documents=chunks,
        ids=[f"{file_name}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file_path} for _ in chunks]
    )
    return f"Added successfully. Collection size: {database.count()}"

def add_file(file_path, file_type):
    file_type = file_type.lower()
    if file_type == "html":
        return add_html(file_path)
    elif file_type == "docx":
        return add_docx(file_path)
    elif file_type == "txt":
        return add_txt(file_path)
    else:
        return "Unsupported file type."

# --- Retrieval ---
def get_context(query, k=3):
    results = database.query(
        query_texts=[query],
        n_results=k
    )
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    context_blocks = [f"[Source: {meta['source']}]\n{doc}" for doc, meta in zip(documents, metadatas)]
    return "\n\n".join(context_blocks)

# --- Chat function ---
def run_rag(user_input):
    context = get_context(user_input)
    messages = [
        {
            "role": "system",
            "content": "Answer the question using ONLY the provided context. If not in context, say you do not know."
        },
        {
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {user_input}"
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
    )
    return response.choices[0].message.content