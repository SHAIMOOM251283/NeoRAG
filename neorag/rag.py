from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

class RAG:
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.docs = self.load_document()
        self.splits = self.split_text()
        self.vectorstore = self.create_embeddings_vector_store()
        self.retriever = self.setup_retriever()
        self.llm = self.setup_llm()
        self.prompt = self.prompt_template()
        self.rag_chain = self.create_rag_chain()

    def load_document(self):
        # No hardcoded path anymore — use the path passed to the class
        loader = PyPDFLoader(self.pdf_path)
        docs = loader.load()
        return docs

    def split_text(self):
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=200)
        splits = text_splitter.split_documents(self.docs)
        return splits

    def create_embeddings_vector_store(self):
        embeddings = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = Chroma.from_documents(
            documents=self.splits,
            embedding=embeddings,
            collection_name="my_rag_collection"   # ← you can make this dynamic later if needed
        )
        return vectorstore
    
    def setup_retriever(self):
        retriever = self.vectorstore.as_retriever(search_kwargs={"k": 3})
        return retriever

    def setup_llm(self):
        llm = ChatOllama(model="llama3.2:1b", temperature=0.7)
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

    def create_rag_chain(self):
        rag_chain = (
            {"context": self.retriever | self.format_docs, "question": RunnablePassthrough()}
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        return rag_chain

    # ────────────────────────────────────────────────
    # New helper method — makes it easy to ask questions
    # ────────────────────────────────────────────────
    def ask(self, question: str) -> str:
        if not question:
            return "Please provide a question."
        try:
            response = self.rag_chain.invoke(question)
            return response
        except Exception as e:
            return f"Error during inference: {str(e)}"