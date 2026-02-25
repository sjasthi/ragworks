from flask import Flask, request, jsonify
from rag_logic import run_rag, add_file

app = Flask(__name__)

# Endpoint to query RAG
@app.route("/query", methods=["POST"])
def query():
    user_input = request.json.get("input", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400
    answer = run_rag(user_input)
    return jsonify({"response": answer})

# Endpoint to upload a file
@app.route("/upload", methods=["POST"])
def upload():
    data = request.json
    file_path = data.get("file_path")
    file_type = data.get("file_type")
    if not file_path or not file_type:
        return jsonify({"error": "Missing file path or type"}), 400
    result = add_file(file_path, file_type)
    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(debug=True)