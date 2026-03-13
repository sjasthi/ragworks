from flask import Flask, request, jsonify
from flask_cors import CORS
from rag_logic import run_rag, add_file, list_documents, delete_document, chroma_stats

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

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


# -- Endpoints for Admin ---
@app.route("/admin/documents", methods=["GET"])
def admin_documents():
    return jsonify({"documents": list_documents()})

@app.route("/admin/stats", methods=["GET"])
def admin_stats():
    return jsonify(chroma_stats())

@app.route("/admin/upload", methods=["POST"])
def admin_upload():
    data = request.json or {}
    file_path = data.get("file_path")
    file_type = data.get("file_type")
    replace = bool(data.get("replace", False))

    if not file_path or not file_type:
        return jsonify({"error": "Missing file path or type"}), 400

    result = add_file(file_path, file_type, replace=replace)
    return jsonify({"result": result})

@app.route("/admin/documents", methods=["DELETE"])
def admin_delete():
    data = request.json or {}
    source = data.get("source")
    if not source:
        return jsonify({"error": "Missing source"}), 400
    result = delete_document(source)
    return jsonify(result)