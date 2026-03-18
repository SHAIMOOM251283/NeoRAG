# app.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import traceback

from rag import RAG

app = Flask(__name__)
CORS(app)

# Global state - we keep one document active at a time
current_rag = None
current_filename = None
current_pdf_path = None

# ────────────────────────────────────────────────
# Serve frontend files
# ────────────────────────────────────────────────

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    """Serve CSS, JS, images, etc."""
    return send_from_directory('.', filename)

# ────────────────────────────────────────────────
# API Endpoints
# ────────────────────────────────────────────────

@app.route("/upload", methods=["POST"])
def upload_pdf():
    global current_rag, current_filename, current_pdf_path

    if "pdf" not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "Only PDF files are allowed"}), 400

    try:
        # Save file persistently (Chroma can reuse embeddings)
        upload_dir = Path("uploaded_pdfs")
        upload_dir.mkdir(exist_ok=True)

        pdf_path = upload_dir / file.filename
        file.save(pdf_path)

        print(f"[upload] Processing PDF: {pdf_path}")

        # ─────────────── Updated RAG instantiation ───────────────
        current_rag = RAG(file_path=str(pdf_path), auto_detect=True)
        print(f"[upload] RAG initialized with loader: {current_rag.loader_type} "
              f"(strategy: {current_rag.unstructured_strategy})")
        # ───────────────────────────────────────────────────────────

        current_filename = file.filename
        current_pdf_path = str(pdf_path)

        return jsonify({
            "success": True,
            "message": "PDF processed and indexed successfully",
            "filename": current_filename
        })

    except Exception as e:
        print("[upload error]", traceback.format_exc())
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
        # Call the chain from your current rag.py (v2)
        answer = current_rag.rag_chain.invoke(question)

        return jsonify({
            "success": True,
            "answer": answer.strip() if isinstance(answer, str) else str(answer)
        })

    except Exception as e:
        print("[ask error]", traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500

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
        "message": "Document is ready (persistent Chroma index)"
    })

@app.route("/clear", methods=["POST"])
def clear():
    global current_rag, current_filename, current_pdf_path
    current_rag = None
    current_filename = None
    current_pdf_path = None
    return jsonify({"success": True, "message": "Current document cleared"})

if __name__ == "__main__":
    print("Starting NeoRAG server ...")
    print("Open in browser: http://localhost:5000/")
    print("Make sure Ollama is running with nomic-embed-text and llama3.2:1b\n")
    app.run(host="0.0.0.0", port=5000, debug=True)