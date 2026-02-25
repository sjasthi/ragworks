
# To test the backend API endpoints you can use this file.

# The server must be running (python app.py) for this to work.
#1. Run python app.py in the terminal to start the server
#2. In another terminal, run this test_backend.py file to see the responses from the API endpoints.
#3. No files have been uploaded yet, so the query response will be based on an empty knowledge base. 
   # You can test the upload endpoint by uncommenting the relevant section and providing a valid file path and type.


## DO NOT commit the _pycache_ or chroma_storage folders to version control, they are generated at runtime and can be ignored.

import requests

while True:
    question = input("Ask your question (or type 'exit' to quit): ")
    if question.lower() == "exit":
        break
    response = requests.post(
        "http://127.0.0.1:5000/query",
        json={"input": question}
    )
    print("RAG:", response.json()["response"])

# Optional: test /upload endpoint
# resp2 = requests.post(
#     "http://127.0.0.1:5000/upload",
#     json={"file_path": "C:/path/to/file.docx", "file_type": "docx"}
# )
# print("Upload response:", resp2.json())