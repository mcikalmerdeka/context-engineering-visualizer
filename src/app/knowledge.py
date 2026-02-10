"""Knowledge base with RAG capabilities"""

import os
from typing import List
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from config import logger_knowledge


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
        
        logger_knowledge.info(f"Initializing KnowledgeBase with embedding_model={embedding_model}, top_k={top_k}")
        logger_knowledge.debug(f"PDF path: {pdf_path}")
        logger_knowledge.debug(f"Index path: {index_path}")
        
        logger_knowledge.info(f"Loading OpenAI embeddings model: {embedding_model}")
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = self._load_or_create_index(recreate_index)
        
    def _load_or_create_index(self, recreate: bool = False) -> FAISS:
        """Load existing FAISS index or create new one from PDF"""
        # If index exists and not recreating, load it
        if not recreate and os.path.exists(self.index_path):
            logger_knowledge.info(f"Loading existing FAISS index from {self.index_path}")
            try:
                vectorstore = FAISS.load_local(
                    self.index_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
                logger_knowledge.info("FAISS index loaded successfully")
                return vectorstore
            except Exception as e:
                logger_knowledge.error(f"Failed to load FAISS index: {str(e)}")
                raise
        
        # Otherwise, create new index
        logger_knowledge.info(f"Creating new FAISS index from {self.pdf_path}")
        
        # Remove old index if recreating
        if recreate and os.path.exists(self.index_path):
            import shutil
            try:
                shutil.rmtree(self.index_path)
                logger_knowledge.info("Removed old index directory")
            except Exception as e:
                logger_knowledge.warning(f"Could not remove old index: {e}")
        
        # Load PDF document
        if not os.path.exists(self.pdf_path):
            error_msg = f"PDF file not found: {self.pdf_path}"
            logger_knowledge.error(error_msg)
            raise FileNotFoundError(error_msg)
        
        logger_knowledge.info(f"Loading PDF from {self.pdf_path}")
        try:
            loader = PyPDFLoader(self.pdf_path)
            documents = loader.load()
            logger_knowledge.info(f"Loaded {len(documents)} pages from PDF")
        except Exception as e:
            logger_knowledge.error(f"Failed to load PDF: {str(e)}")
            raise
        
        # Split documents into chunks using RecursiveCharacterTextSplitter
        logger_knowledge.info("Splitting documents into chunks")
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,  # Optimized for better granularity
            chunk_overlap=150,  # Reduced proportionally
            length_function=len,
            separators=["\n\n", "\n", ". ", ", ", " ", ""]  # Paragraph > Line > Sentence > Clause > Word
        )
        chunks = text_splitter.split_documents(documents)
        logger_knowledge.info(f"Split into {len(chunks)} chunks")
        
        # Create FAISS index from chunks
        logger_knowledge.info("Creating FAISS vector store from chunks")
        try:
            vectorstore = FAISS.from_documents(chunks, self.embeddings)
            logger_knowledge.info("FAISS vector store created successfully")
        except Exception as e:
            logger_knowledge.error(f"Failed to create FAISS vector store: {str(e)}")
            raise
        
        # Save the index
        try:
            vectorstore.save_local(self.index_path)
            logger_knowledge.info(f"Saved FAISS index to {self.index_path}")
        except Exception as e:
            logger_knowledge.error(f"Failed to save FAISS index: {str(e)}")
            raise
        
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
            logger_knowledge.error("Vector store not initialized!")
            return []
        
        k = k or self.top_k
        logger_knowledge.debug(f"Retrieving top {k} documents for query")
        
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            logger_knowledge.info(f"Retrieved {len(results)} documents")
            return results
        except Exception as e:
            logger_knowledge.error(f"Document retrieval failed: {str(e)}")
            raise
    
    def retrieve_relevant(self, query: str, k: int = None) -> str:
        """
        Retrieve relevant documents as formatted string with metadata
        
        Args:
            query: User question
            k: Number of documents to retrieve (uses top_k if not specified)
            
        Returns:
            Concatenated text from relevant documents with metadata
        """
        logger_knowledge.info(f"Retrieving context for query: {query[:50]}..." if len(query) > 50 else f"Retrieving context for query: {query}")
        
        docs = self.retrieve_relevant_docs(query, k)
        
        if not docs:
            logger_knowledge.warning("No documents retrieved for query")
            return ""
        
        formatted_chunks = []
        for i, doc in enumerate(docs, 1):
            chunk_text = f"--- Chunk {i} ---"
            
            # Add metadata if available
            if doc.metadata:
                metadata_str = ", ".join([f"{k}: {v}" for k, v in doc.metadata.items()])
                chunk_text += f"\nMetadata: {metadata_str}"
                logger_knowledge.debug(f"Chunk {i} metadata: {doc.metadata}")
            
            # Add content
            content_preview = doc.page_content[:100] + "..." if len(doc.page_content) > 100 else doc.page_content
            logger_knowledge.debug(f"Chunk {i} content preview: {content_preview}")
            chunk_text += f"\n\n{doc.page_content}"
            formatted_chunks.append(chunk_text)
        
        total_length = sum(len(chunk) for chunk in formatted_chunks)
        logger_knowledge.info(f"Formatted {len(formatted_chunks)} chunks, total length: {total_length} characters")
        
        return "\n\n".join(formatted_chunks)
