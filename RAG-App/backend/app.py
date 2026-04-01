import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from rag_logic import (
    run_rag,
    add_file,
    list_documents,
    delete_document as rag_delete_document,
    chroma_stats,
)

app = Flask(__name__)
CORS(app) # Enable CORS for all routes and origins, allowing the frontend to communicate with the backend without cross-origin issues.

# Define the API endpoint for handling user queries. This endpoint expects a POST request with a JSON body containing the user's input. It processes the input using the run_rag function and returns the response as JSON.
@app.route("/query", methods=["POST"])
def query():
    user_input = request.json.get("input", "")
    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    answer = run_rag(user_input)
    return jsonify({"response": answer})


@app.route("/admin/upload", methods=["POST"])
def upload():
    try:
        data = request.json or {}
        file_path = data.get("file_path", "").strip()
        file_type = data.get("file_type", "").strip().lower()
        replace = data.get("replace", False)

        if not file_path or not file_type:
            return jsonify({"error": "Missing file path or type"}), 400

        if not os.path.isfile(file_path):
            return jsonify({"error": f"File not found: {file_path}"}), 400

        result = add_file(file_path, file_type, replace=replace)
        return jsonify({"result": result}), 200

    except Exception as e:
        print("UPLOAD ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/admin/documents", methods=["GET"])
def get_documents():
    try:
        docs = list_documents()
        return jsonify({"documents": docs}), 200

    except Exception as e:
        print("GET DOCUMENTS ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/admin/stats", methods=["GET"])
def get_admin_stats():
    try:
        stats = chroma_stats()
        return jsonify(stats), 200

    except Exception as e:
        print("STATS ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/admin/documents", methods=["DELETE"])
def delete_admin_document():
    try:
        data = request.json or {}
        source = data.get("source", "").strip()

        if not source:
            return jsonify({"error": "Missing source"}), 400

        result = rag_delete_document(source)
        return jsonify(result), 200

    except Exception as e:
        print("DELETE ERROR:", e)
        return jsonify({"error": str(e)}), 500
    

    #Update a file by re-uploading it with the same name and setting replace=True.
UPLOAD_FOLDER = os.path.abspath("admin_uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/admin/update-document", methods=["POST"])
def update_document():
    try:
        old_source = request.form.get("old_source", "").strip()

        if not old_source:
            return jsonify({"error": "Missing old_source"}), 400

        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if not file or file.filename.strip() == "":
            return jsonify({"error": "No file selected"}), 400

        filename = secure_filename(file.filename)
        if "." not in filename:
            return jsonify({"error": "Uploaded file must have an extension"}), 400

        file_type = filename.rsplit(".", 1)[1].lower()
        allowed_types = {"pdf", "docx", "txt", "html", "pptx"}

        if file_type not in allowed_types:
            return jsonify({"error": f"Unsupported file type: {file_type}"}), 400

        new_file_path = os.path.join(UPLOAD_FOLDER, filename)

        # Overwrite if same filename already exists in uploads folder
        file.save(new_file_path)

        # Delete the old selected document from Chroma
        delete_result = rag_delete_document(old_source)

        # Add the new uploaded file
        add_result = add_file(new_file_path, file_type, replace=True)

        return jsonify({
            "message": "Document updated successfully",
            "deleted": delete_result,
            "added": add_result,
            "new_file_path": new_file_path
        }), 200

    except Exception as e:
        print("UPDATE DOCUMENT ERROR:", e)
        return jsonify({"error": str(e)}), 500

#Running the flask app must be at the end of the file to avoid issues with imports and route definitions. This ensures that all routes are registered before the server starts accepting requests.
if __name__ == "__main__":
    app.run(debug=True)