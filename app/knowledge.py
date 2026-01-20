"""Knowledge base with RAG capabilities"""

import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class KnowledgeBase:
    """Knowledge base with FAISS vector store for RAG capabilities"""
    
    def __init__(self, pdf_path: str, index_path: str, embedding_model: str = "text-embedding-3-small", top_k: int = 2, recreate_index: bool = False):
        """
        Initialize knowledge base with FAISS vector store
        
        Args:
            pdf_path: Path to the PDF document
            index_path: Path to save/load the FAISS index
            embedding_model: OpenAI embedding model to use
            top_k: Number of documents to retrieve
            recreate_index: Whether to recreate the FAISS index from scratch
        """
        self.pdf_path = pdf_path
        self.index_path = index_path
        self.top_k = top_k
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = self._load_or_create_index(recreate_index)
        
    def _load_or_create_index(self, recreate: bool = False) -> FAISS:
        """Load existing FAISS index or create new one from PDF"""
        # If index exists and not recreating, load it
        if not recreate and os.path.exists(self.index_path):
            print(f"Loading existing FAISS index from {self.index_path}")
            return FAISS.load_local(
                self.index_path,
                self.embeddings,
                allow_dangerous_deserialization=True
            )
        
        # Otherwise, create new index
        print(f"Creating new FAISS index from {self.pdf_path}")
        
        # Remove old index if recreating
        if recreate and os.path.exists(self.index_path):
            import shutil
            try:
                shutil.rmtree(self.index_path)
                print("Removed old index directory")
            except Exception as e:
                print(f"Warning: Could not remove old index: {e}")
        
        # Load PDF document
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF file not found: {self.pdf_path}")
        
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from PDF")
        
        # Split documents into chunks using RecursiveCharacterTextSplitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Optimized for better granularity
            chunk_overlap=150,  # Reduced proportionally
            length_function=len,
            separators=["\n\n", "\n", ". ", ", ", " ", ""]  # Paragraph > Line > Sentence > Clause > Word
        )
        chunks = text_splitter.split_documents(documents)
        print(f"Split into {len(chunks)} chunks")
        
        # Create FAISS index from chunks
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        
        # Save the index
        vectorstore.save_local(self.index_path)
        print(f"Saved FAISS index to {self.index_path}")
        
        return vectorstore
    
    def retrieve_relevant_docs(self, query: str, k: int = None) -> List[Document]:
        """
        Retrieve relevant documents for a query
        
        Args:
            query: User question
            k: Number of documents to retrieve (uses top_k if not specified)
            
        Returns:
            List of relevant document chunks
        """
        if not self.vectorstore:
            print("Warning: Vector store not initialized!")
            return []
        
        k = k or self.top_k
        return self.vectorstore.similarity_search(query, k=k)
    
    def retrieve_relevant(self, query: str, k: int = None) -> str:
        """
        Retrieve relevant documents as formatted string with metadata
        
        Args:
            query: User question
            k: Number of documents to retrieve (uses top_k if not specified)
            
        Returns:
            Concatenated text from relevant documents with metadata
        """
        docs = self.retrieve_relevant_docs(query, k)
        
        formatted_chunks = []
        for i, doc in enumerate(docs, 1):
            chunk_text = f"--- Chunk {i} ---"
            
            # Add metadata if available
            if doc.metadata:
                metadata_str = ", ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
                chunk_text += f"\nMetadata: {metadata_str}"
            
            # Add content
            chunk_text += f"\n\n{doc.page_content}"
            formatted_chunks.append(chunk_text)
        
        return "\n\n".join(formatted_chunks)
