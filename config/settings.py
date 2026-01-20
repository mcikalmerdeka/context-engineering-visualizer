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
    
    # Memory Settings
    MAX_CONVERSATION_MESSAGES = 4
    
    # RAG Settings
    RAG_TOP_K = 2
    
    # UI Settings
    GRADIO_SHARE = False
    GRADIO_SERVER_NAME = "0.0.0.0"
    GRADIO_SERVER_PORT = 7860
    
    # System Prompt
    SYSTEM_PROMPT = """You are a data analyst assistant.

Your role:
- Answer questions about business metrics and data analysis
- Use the provided context and knowledge to give accurate answers
- If context is insufficient, clearly state what information is missing
- Always explain your reasoning briefly
- Use the calculator tool for numeric computations

Be concise, accurate, and helpful."""
