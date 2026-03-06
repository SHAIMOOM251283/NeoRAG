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
        
        self.loader_type = loader_type
        self.unstructured_strategy = unstructured_strategy
        self.auto_detect = auto_detect
        
        self.docs = self.load_document()
        print(f"Loaded {len(self.docs)} documents.")  # Debug
        if self.docs:
            print(f"Sample content: {self.docs[0].page_content[:100]}...")  # Debug
        
        self.splits = self.split_text()
        print(f"Created {len(self.splits)} splits.")  # Debug
        if self.splits:
            print(f"First split preview: {self.splits[0].page_content[:200]}...")  # Debug
        
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
                mode="elements",           # Preserves structure (headings, tables, etc.)
                languages=["eng"]          # Specify English to suppress warning and improve OCR
            )
        else:
            raise ValueError("Invalid loader_type. Choose 'pypdf', 'pymupdf', or 'unstructured'.")
        
        docs = loader.load()
        if not docs:
            print("Warning: No content loaded from PDF. Check if PDF has extractable text.")
        return docs

    def _auto_detect_and_load(self):
        """
        Tries loaders in order of speed → capability:
        1. PyMuPDF (fastest, good for most text PDFs)
        2. PyPDF
        3. Unstructured (fast)
        4. Unstructured (hi_res) — best for complex/scanned PDFs but slowest
        """
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
                
                if docs and total_content_length > 200:  # reasonable minimum threshold
                    print(f"Auto-detect SUCCESS with {loader_type} (strategy={strategy})")
                    print(f"Extracted {total_content_length} characters of content.")
                    self.loader_type = loader_type           # Update for split_text consistency
                    self.unstructured_strategy = strategy
                    return docs
                
                else:
                    print(f" → Empty or very little content. Trying next...")
                    
            except Exception as e:
                print(f" → Failed: {str(e)}")
        
        raise ValueError(
            "Auto-detect failed: Could not extract meaningful content from PDF "
            "with any available loader. Try specifying loader_type manually."
        )

    def split_text(self):
        if self.loader_type == "unstructured" and self.unstructured_strategy == "hi_res":
            # Skip further splitting for hi_res — preserves semantic elements
            print("Using hi_res unstructured loader → skipping text splitting")
            return self.docs
        else:
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=1000,
                chunk_overlap=200
            )
            splits = text_splitter.split_documents(self.docs)
            return splits

    def create_embeddings_vector_store(self):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        persist_dir = Path("chroma_db").resolve()
        
        if persist_dir.exists():
            print("Loading existing Chroma DB...")
            vectorstore = Chroma(
                persist_directory=str(persist_dir),
                embedding_function=embeddings,
                collection_name="my_rag_collection"
            )
        else:
            print("Creating new Chroma DB...")
            vectorstore = Chroma(
                persist_directory=str(persist_dir),
                embedding_function=embeddings,
                collection_name="my_rag_collection"
            )

            filtered_splits = filter_complex_metadata(self.splits)

            # Batch add to avoid RAM issues
            batch_size = 50
            for i in range(0, len(filtered_splits), batch_size):
                batch = filtered_splits[i:i + batch_size]
                vectorstore.add_documents(batch)
                print(f"Added batch {i//batch_size + 1} / {((len(filtered_splits)-1)//batch_size)+1}")
        
        return vectorstore
    
    def setup_retriever(self):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 6})
        return retriever

    def setup_llm(self):
        llm = ChatOllama(model="llama3.2:1b", temperature=0.5)
        return llm

    def prompt_template(self):
        prompt = ChatPromptTemplate.from_template(
            """Answer the question based ONLY on the following context. 
            If you don't know, say you don't know.
    
            Context: {context}
    
            Question: {question}
    
            Answer:"""
        )
        return prompt

    def format_docs(self, docs):
        return "\n\n".join(doc.page_content for doc in docs)

    def create_RAG_chain(self):
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    def run(self):
        print("\n📚 RAG System Ready (type 'q' to exit)\n")

        while True:
            question = input("Enter Question: ").strip()

            if question.lower() == "q":
                print("Exiting RAG system...")
                break

            if not question:
                print("Please enter a valid question.\n")
                continue

            try:
                response = self.rag_chain.invoke(question)
                print("\nAnswer:\n", response, "\n")
            except Exception as e:
                print("Error:", e)


if __name__ == '__main__':
    # Examples of how to use:
    
    # 1. Default (PyMuPDF)
    # rag = RAG()
    
    # 2. Explicit choice
    # rag = RAG(loader_type="unstructured", unstructured_strategy="hi_res")
    
    # 3. Let it try to auto-detect the best loader
    rag = RAG(auto_detect=True)
    
    rag.run()