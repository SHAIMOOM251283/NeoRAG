# **NeoRAG – PDF Question-Answering with RAG**

A clean, **local** web application that lets you upload any PDF document and ask natural-language questions about its content — powered by **Retrieval-Augmented Generation (RAG)**.

## NeoRAG Screenhots 

![NeoRAG Screenshot](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/image_1.png)  
![NeoRAG Screenshot](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/image_2.png)
![NeoRAG Screenshot](https://github.com/SHAIMOOM251283/NeoRAG/blob/main/images/image_3.png)

## Features

- Modern neon/cyberpunk-style interface
- Drag-and-drop or click-to-upload PDF files
- Real-time document indexing & question answering
- "Clear & Upload New" button to reset and start over
- Animated particle background
- Responsive design
- 100% local — no cloud services required

## Tech Stack

**Backend**  
- Python 3.10+  
- Flask  
- LangChain + Ollama integration  
- Chroma (in-memory vector store)  

**Frontend**  
- HTML5 + CSS3 (custom neon theme)  
- Vanilla JavaScript (no frameworks)  

**Local AI** (via Ollama)  
- Embeddings: `nomic-embed-text`  
- LLM: `llama3.2:1b` (very lightweight)

## Prerequisites

1. **Python 3.10+**  
2. **Ollama** (required – runs the embedding & generation models locally)  
   - Download and install from: https://ollama.com/download  
   - After installation, open a terminal and pull the required models:  
     ```bash
     ollama pull nomic-embed-text
     ollama pull llama3.2:1b
     ```
   - Start the Ollama server (keep this running in a separate terminal):  
     ```bash
     ollama serve
     ```

## Installation

```bash
# Clone the repository
git clone https://github.com/SHAIMOOM251283/NeoRAG.git
cd NeoRAG

# Go into the project folder
cd neorag

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate          # Linux/macOS
# or on Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt
```

## Running the App

1. Make sure Ollama is running (`ollama serve` in another terminal)  
2. Start the web server:

```bash
python app.py
```

3. Open your browser and go to:  
   **http://localhost:5000/**


## Project Structure

NeoRAG/                     # Repository root
├── images/                 # Application screenshots
│   ├── screenshot1.png     (example names — yours may differ)
│   ├── screenshot2.png
│   └── screenshot3.png
├── neorag/                 # Core application code
│   ├── app.py              # Flask server & API endpoints
│   ├── rag.py              # RAG pipeline (loading, chunking, embedding, querying)
│   ├── index.html          # Main frontend page
│   ├── styles.css          # Neon/cyberpunk styling
│   ├── script.js           # Frontend behavior (upload, chat, particles)
│   ├── requirements.txt    # Python dependencies
│   └── .gitignore          # Ignore patterns (venv, pycache, etc.)
├── LICENSE                 # Project license (MIT recommended)
└── README.md               # This file               

## How It Works (High-Level)

1. Upload PDF → temporary file saved  
2. `rag.py` loads → chunks → embeds → indexes in Chroma  
3. Questions → retrieve relevant chunks → prompt → answer with llama3.2:1b  
4. "Clear & Upload New" resets the current document

## Current Limitations

- Single document active at a time  
- Vector store is in-memory only (lost on server restart)  
- Designed for personal/local use

## Planned / Possible Improvements

- Persistent vector store (save/load Chroma to disk)  
- Multiple documents / document selector  
- Source citation / chunk highlighting in answers  
- File size validation & progress indicators  
- Optional dark/light mode toggle  

## License

MIT

Feel free to fork, modify, and use.

Built in Dhaka with curiosity & local LLMs.  
2025–2026

```