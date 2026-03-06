from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
import traceback

from rag import RAG

app = Flask(__name__)
CORS(app)

current_rag = None
current_filename = None
current_pdf_path = None


@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')


@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('.', filename)


@app.route("/upload", methods=["POST"])
def upload_pdf():
    global current_rag, current_filename, current_pdf_path

    if "pdf" not in request.files:
        return jsonify({"success": False, "error": "No file part"}), 400

    file = request.files["pdf"]
    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"success": False, "error": "Only PDF files allowed"}), 400

    try:
        upload_dir = Path("uploaded_pdfs")
        upload_dir.mkdir(exist_ok=True)

        pdf_path = upload_dir / file.filename
        file.save(pdf_path)

        print(f"[upload] Processing: {pdf_path}")

        current_rag = RAG(file_path=str(pdf_path))
        # current_rag = RAG(file_path=str(pdf_path), auto_detect=True)  # ← optional

        current_filename = file.filename
        current_pdf_path = str(pdf_path)

        return jsonify({
            "success": True,
            "message": "PDF indexed",
            "filename": current_filename
        })

    except Exception as e:
        print("[upload error]", traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/ask", methods=["POST"])
def ask():
    global current_rag

    if current_rag is None:
        return jsonify({"success": False, "error": "No document loaded"}), 400

    data = request.get_json(silent=True)
    if not data or "question" not in data:
        return jsonify({"success": False, "error": "Missing question"}), 400

    question = data["question"].strip()
    if not question:
        return jsonify({"success": False, "error": "Empty question"}), 400

    try:
        answer = current_rag.rag_chain.invoke(question)
        return jsonify({
            "success": True,
            "answer": str(answer).strip()
        })
    except Exception as e:
        print("[ask error]", traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/status", methods=["GET"])
def status():
    if current_rag is None:
        return jsonify({"has_document": False, "message": "No document"})
    return jsonify({
        "has_document": True,
        "filename": current_filename,
        "message": "Ready"
    })


@app.route("/clear", methods=["POST"])
def clear():
    global current_rag, current_filename, current_pdf_path
    current_rag = None
    current_filename = None
    current_pdf_path = None
    return jsonify({"success": True, "message": "Session cleared"})


if __name__ == "__main__":
    print("NeoRAG server")
    print("http://localhost:5000/")
    app.run(host="0.0.0.0", port=5000, debug=True)