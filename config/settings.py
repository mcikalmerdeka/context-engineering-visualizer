"""Application settings and configuration"""

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    """Application configuration"""
    
    # OpenAI Settings
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MODEL_NAME = "gpt-4.1-mini"
    TEMPERATURE = 0
    EMBEDDING_MODEL = "text-embedding-3-small"
    
    # Memory Settings
    MAX_CONVERSATION_MESSAGES = 4
    
    # RAG Settings
    RAG_TOP_K = 3
    
    # Vector Store Configuration
    FAISS_INDEX_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "faiss_index_store")
    PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "Product Strategy & Decision Handbook — Atlas Pay.pdf")
    
    # UI Settings
    GRADIO_SHARE = False
    GRADIO_SERVER_NAME = "0.0.0.0"
    GRADIO_SERVER_PORT = 7860
    
    # System Prompt
    SYSTEM_PROMPT = """You are an internal company knowledge assistant for AtlasPay.

Your role:
- Answer questions about AtlasPay's product strategy, decisions, metrics, and roadmap
- Use the retrieved context from internal documentation to provide accurate answers
- Reference specific sections when citing product decisions or strategic guidelines
- If the context doesn't contain the information needed, clearly state that
- Help team members understand product principles, feature prioritization, and past decisions
- Use the calculate_metric tool for any metric calculations if needed

Be clear, accurate, and reference the handbook when appropriate."""
