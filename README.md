# **NeoRAG – PDF Question-Answering with RAG**

A clean, **local** web application that lets you upload any PDF document and ask natural-language questions about its content — powered by **Retrieval-Augmented Generation (RAG)**.

---

# 🚀 Project Evolution

NeoRAG has evolved into two versions:

* **neorag_v1/** → Initial implementation (basic RAG pipeline, English-only)
* **neorag_v2/** → Improved system with intelligent parsing, persistence, multilingual support, and enhanced UX

---

# 🧩 NeoRAG v1 (Initial Version)

## Screenshots

![v1 Home Page](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v1/home.png)
*Home page / PDF upload*

![v1 Indexing](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v1/indexing.png)
*“Indexing Consciousness” overlay*

![v1 Sample Q\&A](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v1/output_en.png)
*Example Q&A output (English)*

---

## Features

* Modern neon/cyberpunk-style interface
* Drag-and-drop or click-to-upload PDF files
* Real-time document indexing & question answering
* Animated particle background
* Responsive design
* 100% local — no cloud services required

---

## Tech Stack

**Backend**

* Python 3.10+
* Flask
* LangChain + Ollama integration
* Chroma (**in-memory vector store**)

**Frontend**

* HTML5 + CSS3 (custom neon theme)
* Vanilla JavaScript (no frameworks)

**Local AI (via Ollama)**

* Embeddings: `nomic-embed-text`
* LLM: `llama3.2:1b`

---

## Limitations (v1)

* Single document active at a time
* Vector store is **in-memory only** (lost on restart)
* Manual PDF loader selection
* Limited handling of complex/scanned PDFs
* **English-only** — cannot handle PDFs in other languages

---

# ✨ NeoRAG v2 (Improved Version)

> NeoRAG v2 transforms the project into a more **robust and adaptive RAG system** with better document handling, persistence, multilingual support, and performance enhancements.

---

## Screenshots

![v2 Home Page](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v2/home.png)
*Home page / PDF upload (same as v1)*

![v2 Indexing](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v2/indexing.png)
*“Indexing Consciousness” overlay (same as v1)*

![v2 Sample Q\&A (English)](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v2/output_en.png)
*Example Q&A output (English)*

![v2 Sample Q\&A (French)](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/v2/output_fr.png)
*Example Q&A output (French — demonstrates multilingual support)*

---

## 🔥 New & Improved Features

### 🧠 Intelligent PDF Processing

* Automatic loader detection:

  * PyMuPDF (fast)
  * PyPDF
  * Unstructured (fast / hi_res)

* Handles:

  * Clean PDFs
  * Complex layouts
  * Scanned documents

---

### 💾 Persistent Vector Store

* Chroma database stored on disk (`chroma_db/`)
* Reuses embeddings across sessions
* Faster reload and improved efficiency

---

### ⚡ Performance Improvements

* Batch embedding to reduce memory usage
* Smarter chunking strategy
* Skips splitting for structured (`hi_res`) documents

---

### 🌐 Multilingual Support

* Process PDFs in multiple languages
* Output answers in the same language as the PDF content
* English, Spanish, French, and more

---

### 💬 Enhanced Chat & Backend

* **Frontend / UX Improvements**

  * Interactive Q&A chat UI
  * Real-time responses
  * Upgraded loading indicators for better UX

* **Backend Enhancements**

  * Persistent PDF storage (`uploaded_pdfs/`)
  * Automatic PDF loader detection (PyMuPDF / PyPDF / Unstructured)
  * Multi-language support (English, Spanish, French, etc.)
  * Smarter retrieval and RAG chain integration
  * Improved error handling and logging

* **Performance Boosts**

  * Persistent vector store improves `/ask` performance
  * Smarter chunking and batch embedding

---

### 🛡️ Improved Reliability

* Automatic fallback if PDF parsing fails
* Content validation before indexing
* Better debugging logs and error messages

---

## Project Structure

```
NeoRAG/
├── images/
│   ├── v1/
│   │   ├── home.png
│   │   ├── indexing.png
│   │   └── output_en.png
│   ├── v2/
│   │   ├── home.png
│   │   ├── indexing.png
│   │   ├── output_en.png
│   │   └── output_es.png
├── neorag_v1/
│   ├── app.py
│   ├── rag.py
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── requirements.txt
├── neorag_v2/
│   ├── app.py
│   ├── rag.py
│   ├── index.html
│   ├── styles.css
│   ├── script.js
│   └── requirements.txt
├── LICENSE
└── README.md
```

---

## How It Works (High-Level)

1. Upload PDF → temporary file saved
2. RAG system loads → chunks → embeds → indexes in Chroma (persistent in v2)
3. Questions → retrieve relevant chunks → prompt → answer with llama3.2:1b
4. v2 automatically detects loader and handles multilingual PDFs

---

## Prerequisites

1. **Python 3.10+**
2. **Ollama** (runs embedding & generation models locally)

   ```bash
   ollama pull nomic-embed-text
   ollama pull llama3.2:1b
   ollama serve
   ```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/SHAIMOOM251283/NeoRAG.git
cd NeoRAG/neorag_v2  # or neorag_v1 for version 1

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# or on Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the App

```bash
# Make sure Ollama is running
ollama serve

# Start Flask server
python app.py
```

Open your browser at: **[http://localhost:5000/](http://localhost:5000/)**

---

## License

MIT — feel free to fork, modify, and use.

Built in Dhaka with curiosity & local LLMs.
2025–2026

---