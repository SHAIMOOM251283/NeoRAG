from langchain_community.document_loaders import PyPDFLoader, PyMuPDFLoader, UnstructuredPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_community.vectorstores.utils import filter_complex_metadata
from pathlib import Path
import re

class RAG:
    def __init__(
        self,
        file_path="notes.pdf",
        loader_type="pymupdf",
        unstructured_strategy="fast",
        auto_detect=False
    ):
        self.pdf_path = Path(file_path).resolve()
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {self.pdf_path}")

        # Create safe collection name from filename
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', self.pdf_path.stem.lower())
        self.collection_name = f"rag_{safe_name}"

        self.loader_type = loader_type
        self.unstructured_strategy = unstructured_strategy
        self.auto_detect = auto_detect

        self.docs = self.load_document()
        print(f"Loaded {len(self.docs)} documents.")
        if self.docs:
            print(f"Sample content: {self.docs[0].page_content[:100]}...")

        self.splits = self.split_text()
        print(f"Created {len(self.splits)} splits.")
        if self.splits:
            print(f"First split preview: {self.splits[0].page_content[:200]}...")

        self.vectorstore = self.create_embeddings_vector_store()
        self.retriever = self.setup_retriever()
        self.llm = self.setup_llm()
        self.prompt = self.prompt_template()
        self.rag_chain = self.create_RAG_chain()

    def load_document(self):
        if self.auto_detect:
            return self._auto_detect_and_load()

        if self.loader_type == "pypdf":
            loader = PyPDFLoader(str(self.pdf_path))
        elif self.loader_type == "pymupdf":
            loader = PyMuPDFLoader(str(self.pdf_path))
        elif self.loader_type == "unstructured":
            loader = UnstructuredPDFLoader(
                str(self.pdf_path),
                strategy=self.unstructured_strategy,
                mode="elements",
                languages=["eng"]
            )
        else:
            raise ValueError("Invalid loader_type. Choose 'pypdf', 'pymupdf', or 'unstructured'.")

        docs = loader.load()
        if not docs:
            print("Warning: No content loaded from PDF.")
        return docs

    def _auto_detect_and_load(self):
        attempts = [
            ("pymupdf", None),
            ("pypdf", None),
            ("unstructured", "fast"),
            ("unstructured", "hi_res"),
        ]

        for loader_type, strategy in attempts:
            print(f"Auto-detect: Trying {loader_type} (strategy={strategy})...")
            try:
                if loader_type == "pypdf":
                    loader = PyPDFLoader(str(self.pdf_path))
                elif loader_type == "pymupdf":
                    loader = PyMuPDFLoader(str(self.pdf_path))
                elif loader_type == "unstructured":
                    loader = UnstructuredPDFLoader(
                        str(self.pdf_path),
                        strategy=strategy,
                        mode="elements",
                        languages=["eng"]
                    )

                docs = loader.load()
                total_content_length = sum(len(doc.page_content.strip()) for doc in docs)

                if docs and total_content_length > 200:
                    print(f"Auto-detect SUCCESS with {loader_type}")
                    self.loader_type = loader_type
                    self.unstructured_strategy = strategy
                    return docs
                else:
                    print(" → Empty or very little content. Trying next...")
            except Exception as e:
                print(f" → Failed: {str(e)}")

        raise ValueError("Auto-detect failed: Could not extract content.")

    def split_text(self):
        if self.loader_type == "unstructured" and self.unstructured_strategy == "hi_res":
            print("Using hi_res → skipping text splitting")
            return self.docs
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            return text_splitter.split_documents(self.docs)

    def create_embeddings_vector_store(self):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        persist_dir = Path("chroma_db").resolve()

        print(f"Using collection: {self.collection_name}")

        vectorstore = Chroma(
            persist_directory=str(persist_dir),
            embedding_function=embeddings,
            collection_name=self.collection_name
        )

        # Only index if collection is empty
        if vectorstore._collection.count() == 0:
            print("Creating new collection / indexing documents...")
            filtered_splits = filter_complex_metadata(self.splits)
            batch_size = 50
            for i in range(0, len(filtered_splits), batch_size):
                batch = filtered_splits[i:i + batch_size]
                vectorstore.add_documents(batch)
                print(f"Added batch {i//batch_size + 1}")
        else:
            print("Reusing existing collection")

        return vectorstore

    def setup_retriever(self):
        return self.vectorstore.as_retriever(search_kwargs={"k": 6})

    def setup_llm(self):
        return ChatOllama(model="llama3.2:1b", temperature=0.5)  # ← changed to llama2

    def prompt_template(self):
        return ChatPromptTemplate.from_template(
            """Answer the question based ONLY on the following context. 
            If you don't know, say you don't know.

            Context: {context}

            Question: {question}

            Answer:"""
        )

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def create_RAG_chain(self):
        return (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )

    def run(self):
        print("\n📚 RAG System Ready (type 'q' to exit)\n")
        while True:
            question = input("Enter Question: ").strip()
            if question.lower() == "q":
                print("Exiting...")
                break
            if not question:
                continue
            try:
                response = self.rag_chain.invoke(question)
                print("\nAnswer:\n", response, "\n")
            except Exception as e:
                print("Error:", e)


if __name__ == '__main__':
    rag = RAG(auto_detect=True)
    rag.run()