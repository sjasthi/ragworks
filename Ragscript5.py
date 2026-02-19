
## Group - Giraffes
## RAG Script using DOCX File + Persistent ChromaDB (One-at-a-Time Upload)

import os
from openai import OpenAI
from docx import Document
import chromadb
from chromadb.config import Settings


# OpenAI Client

key = input("Enter your OpenAI API key: ").strip()
client = OpenAI(api_key=key)


# Persistent ChromaDB Only while the script is running

script_dir = os.path.dirname(os.path.abspath(__file__))
persist_dir = os.path.join(script_dir, "chroma_storage")

chroma_client = chromadb.Client(
    Settings(persist_directory=persist_dir, anonymized_telemetry=False)
)

collection = chroma_client.get_or_create_collection(
    name="docx_rag_collection"
)
print("Persistent Chroma collection at:", persist_dir)
print("Total stored chunks so far:", collection.count())


# Document Upload Loop

while True:
    add_file = input("\nDo you want to add a DOCX file? (yes/no): ").strip().lower()
    if add_file not in ["yes", "y"]:
        break

    file_path = input("Enter the path to your .docx file: ").strip()
    if not os.path.exists(file_path):
        print("File not found. Try again.")
        continue

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

    # Add to collection with unique IDs and metadata
    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"{file_name}_chunk_{i}" for i in range(len(chunks))],
        metadatas=[{"source": file_name} for _ in chunks]
    )

    print(f"{file_name} added successfully. Total stored chunks now: {collection.count()}")


# Question Loop

print("\nAll documents stored. Ask questions about them!")
print("Type 'exit' to quit.\n")

while True:
    question = input("You: ").strip()
    if question.lower() == "exit":
        print("Goodbye!")
        break

    # Embed question
    question_embedding = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    ).data[0].embedding

    # Retrieve relevant chunks from ALL stored documents
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=10  # Increase if you have many chunks
    )

    # Flatten all returned chunks
    context_chunks = []
    for doc_list in results["documents"]:
        context_chunks.extend(doc_list)

    context = "\n".join(context_chunks)

    # Prompt the LLM
    prompt = f"""
Use the context below to answer the question.
If the answer is not in the context, say you don't know.

Context:
{context}

Question:
{question}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    print("\nRAG:", response.choices[0].message.content, "\n")
