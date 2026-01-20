"""Utility script to process PDF and create FAISS index"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.settings import Settings
from app.knowledge import KnowledgeBase


def main():
    """Process PDF and create FAISS index"""
    print("=" * 60)
    print("Processing Knowledge Base PDF")
    print("=" * 60)
    
    # Initialize knowledge base with recreate_index=True
    kb = KnowledgeBase(
        pdf_path=Settings.PDF_PATH,
        index_path=Settings.FAISS_INDEX_PATH,
        embedding_model=Settings.EMBEDDING_MODEL,
        top_k=Settings.RAG_TOP_K,
        recreate_index=True
    )
    
    print("\n" + "=" * 60)
    print("Knowledge Base Created Successfully!")
    print("=" * 60)
    
    # Display all chunks created
    print("\n" + "=" * 60)
    print("Displaying All Created Chunks")
    print("=" * 60)
    
    # Get all documents from the vector store
    all_docs = kb.vectorstore.docstore._dict
    total_chunks = len(all_docs)
    
    print(f"\nTotal chunks created: {total_chunks}\n")
    
    for i, (_, doc) in enumerate(all_docs.items(), 1):
        print(f"\n{'─' * 60}")
        print(f"CHUNK {i}/{total_chunks}")
        print(f"{'─' * 60}")
        
        # Display metadata (page number, source)
        if doc.metadata:
            print(f"Metadata: {doc.metadata}")
        
        # Display full content
        content = doc.page_content
        print(f"\nContent ({len(content)} chars):")
        print(content)
    
    # Display summary statistics
    print("\n" + "=" * 60)
    print("Chunk Statistics")
    print("=" * 60)
    
    chunk_lengths = [len(doc.page_content) for doc in all_docs.values()]
    avg_length = sum(chunk_lengths) / len(chunk_lengths)
    min_length = min(chunk_lengths)
    max_length = max(chunk_lengths)
    
    print(f"\nTotal chunks: {total_chunks}")
    print(f"Average chunk length: {avg_length:.0f} characters")
    print(f"Min chunk length: {min_length} characters")
    print(f"Max chunk length: {max_length} characters")
    
    # Count chunks by page
    pages = {}
    for doc in all_docs.values():
        page = doc.metadata.get('page', 'unknown')
        pages[page] = pages.get(page, 0) + 1
    
    print(f"\nChunks by page:")
    for page in sorted(pages.keys()):
        print(f"  Page {page}: {pages[page]} chunks")
    
    # Test retrieval
    print("\n" + "=" * 60)
    print("Testing Retrieval")
    print("=" * 60)
    
    test_query = "What is product strategy?"
    results = kb.retrieve_relevant(test_query)
    print(f"\nQuery: {test_query}")
    print(f"\nRetrieved context:\n{results}")


if __name__ == "__main__":
    main()
