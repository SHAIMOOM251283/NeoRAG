# Optional: keep this for local testing / debugging
if __name__ == "__main__":
    # Example usage (you can remove this block later)
    import sys
    if len(sys.argv) > 1:
        pdf_file = sys.argv[1]
        rag = RAG(pdf_path=pdf_file)
        print("RAG ready. Type your question (or 'q' to quit):")
        while True:
            q = input("> ").strip()
            if q.lower() in ['q', 'quit', 'exit']:
                break
            if q:
                print("\nAnswer:", rag.ask(q), "\n")
    else:
        print("Usage: python rag.py <path_to_pdf>")

# test_rag.py (create this file only when you want to test manually)
from rag import RAG

if __name__ == "__main__":
    pdf = "path/to/your/notes.pdf"
    rag = RAG(pdf_path=pdf)
    while True:
        q = input("Question: ").strip()
        if q.lower() in ['q', 'quit']: break
        print(rag.ask(q))