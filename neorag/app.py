# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import tempfile
from pathlib import Path

from rag import RAG

app = Flask(__name__)
CORS(app)  # Allows frontend running on different port/origin

# Global state - simple for single-user / in-memory use
current_rag = None
current_filename = None


@app.route("/upload", methods=["POST"])
def upload_pdf():
    global current_rag, current_filename

    if "pdf" not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "Only PDF files are allowed"}), 400

    # Save to temporary file
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            file.save(tmp.name)
            pdf_path = tmp.name

        # Create RAG instance
        current_rag = RAG(pdf_path=pdf_path)
        current_filename = file.filename

        # Optional: remove the temp file after loading
        # (Chroma keeps data in memory, so file is no longer needed)
        try:
            os.unlink(pdf_path)
        except:
            pass  # not critical if deletion fails

        return jsonify({
            "success": True,
            "message": "PDF processed successfully",
            "filename": current_filename
        })

    except Exception as e:
        # Clean up temp file on error
        if "pdf_path" in locals():
            try:
                os.unlink(pdf_path)
            except:
                pass
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    global current_rag

    if current_rag is None:
        return jsonify({"success": False, "error": "No document loaded. Please upload a PDF first."}), 400

    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"success": False, "error": "Missing or invalid question"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"success": False, "error": "Question cannot be empty"}), 400

    try:
        answer = current_rag.ask(question)
        return jsonify({
            "success": True,
            "answer": answer
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Processing error: {str(e)}"}), 500


@app.route("/status", methods=["GET"])
def status():
    if current_rag is None:
        return jsonify({
            "has_document": False,
            "message": "No document loaded"
        })
    return jsonify({
        "has_document": True,
        "filename": current_filename,
        "message": "Document is ready"
    })


@app.route("/clear", methods=["POST"])
def clear():
    global current_rag, current_filename
    current_rag = None
    current_filename = None
    return jsonify({"success": True, "message": "Current document cleared"})


if __name__ == "__main__":
    print("Starting NeoRAG server...")
    app.run(host="0.0.0.0", port=5000, debug=True)