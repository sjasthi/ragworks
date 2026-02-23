# This project implements a RAG framework that allows users to:
# 1. Upload a set of documents (PDFs, Word, HTML, text, etc)
# 2. Automatically preprocess and embed them into a retrievable knowledge store
# 3. Ask questions in natural language and get grounded, source-referenced responses

import os
from openai import OpenAI, AuthenticationError
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from docx import Document
import chromadb
from chromadb.utils import embedding_functions
from chromadb.config import Settings

# OpenAI Client
def create_client(api_key):
    try:
        client = OpenAI(api_key=api_key)
        client.models.list()
        return client
    except AuthenticationError:
        print("Invalid API")
    return None
load_dotenv()

# Load api key
api_key = os.environ.get("OPENAI_KEY")
if not api_key:
    api_key = input("Enter your OpenAI API key: ").strip()

client = create_client(api_key)

# Persistent ChromaDB only while the script is running
script_dir = os.path.dirname(os.path.abspath(__file__))
persist_dir = os.path.join(script_dir, "chroma_storage")

chroma_client = chromadb.Client(
    Settings(persist_directory=persist_dir, anonymized_telemetry=False)
)

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small"
)

database = chroma_client.get_or_create_collection(
    name="RAG_Work_test",
    embedding_function=openai_ef
)

print("Persistent Chroma collection at:", persist_dir)
print("Total stored chunks so far:", database.count())

# HTML ingestion - using soup to extract the text from it
def add_html(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")
    htm_txt = soup.get_text(strip=True)

    database.add(
        documents=[htm_txt],
        metadatas=[{"source": file_path}],
        ids=[f"html_{os.path.basename(file_path)}"]
    )

    print(f"{file_path} added successfully. Total stored chunks now: {database.count()}")

# DOCX ingestion
def add_docx(file_path):
    file_name = os.path.splitext(os.path.basename(file_path))[0]

    # Load DOCX
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])

    # Chunk Text
    chunk_size = 500
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

    # Create Embeddings
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=chunks
    )
    embeddings = [item.embedding for item in response.data]

    # Add to collection with unique IDS and metadata
    database.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{file_name}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file_name} for _ in chunks]
    )

    print(f"{file_path} added successfully. Total stored chunks now: {database.count()}")

# TXT Ingestion
def add_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()

    chunks = [sentence.strip() for sentence in content.split(".") if sentence]

    print("Chunks:", chunks)

    database.add(
        documents=chunks,
        ids=[f"txt_doc{i}" for i in range(len(chunks))],
        metadatas=[{"source": file_path}] * len(chunks)
    )

    print(f"{file_path} added successfully. Total stored chunks now: {database.count()}")

# Retrieval
def get_context(query):
    results = database.query(
        query_texts=[query],
        n_results=3, # gives top 3 relevant matches to the query
    )
    # querying the database with relevant info then extracting
    if results["documents"] and results["documents"][0]:
        context = "\n\n".join(results["documents"][0])
        return context
    return ""

# Chat
def chat(user_input):
    context = get_context(user_input)

    msg = [{
        "role": "developer",
        "content": "Talk like an assistant, use the context to answer the question."
    }]

    if context:
        msg.append({
            "role": "user",
            "content": f"Context:\n{context}\n\nQuestion: {user_input}"
        })
    else:
        msg.append({"role": "user", "content": user_input})

    comp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=msg,
    )
    response = comp.choices[0].message.content
    return response

# Loop for uploading files
while True:
    add_file = input("\nWhat type of file do you want to add? (html/docx/txt/none): ").strip().lower()
    if add_file == "none":
        break

    file_path = input("Enter the path to your file: ").strip()

    if not os.path.exists(file_path):
        print("File not found. Try again.")
        continue

    if add_file == "html":
        add_html(file_path)
    elif add_file == "docx":
        add_docx(file_path)
    elif add_file == "txt":
        add_txt(file_path)
    else:
        print("Type html, docx, txt, or none")

# Chat loop
print("\nRAG READY. Type exit to quit or file to add a new file")

while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("RAG: Goodbye!")
        break
    elif user_input.lower() == 'file': # added incase the user wants to go back and add another file
        while True:
            add_file = input("\nWhat type of file do you want to add? (html/docx/txt/none): ").strip().lower()
            if add_file == "none":
                break
            file_path = input("Enter the path to your file: ").strip()
            
            if not os.path.exists(file_path):
                print("File not found. Try again.")
                continue

            if add_file == "html":
                add_html(file_path)
            elif add_file == "docx":
                add_docx(file_path)
            elif add_file == "txt":
                add_txt(file_path)
            else:
                print("Type html, docx, txt, or none")     
    else: # any time i typed none, the bot replied immediatly, had to add an else here to fix it
        assistant_rply = chat(user_input)
        print("RAG:", assistant_rply, "\nAnything else needed?")

