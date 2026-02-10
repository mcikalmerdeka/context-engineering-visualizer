"""Conversation memory management"""

from typing import List
from langchain.messages import HumanMessage, AIMessage
from config import logger_memory


class ConversationMemory:
    """Manages conversation history with smart truncation"""
    
    def __init__(self, max_messages: int = 4):
        self.messages = []
        self.max_messages = max_messages
        logger_memory.info(f"ConversationMemory initialized with max_messages={max_messages}")
        
    def add_user_message(self, content: str):
        """Add user message to history"""
        logger_memory.debug(f"Adding user message: {content[:50]}..." if len(content) > 50 else f"Adding user message: {content}")
        self.messages.append(HumanMessage(content=content))
        current_count = len(self.messages)
        logger_memory.info(f"User message added. Current message count: {current_count}")
        self._truncate()
        
    def add_ai_message(self, content: str):
        """Add AI message to history"""
        content_preview = content[:50] + "..." if len(content) > 50 else content
        logger_memory.debug(f"Adding AI message: {content_preview}")
        self.messages.append(AIMessage(content=content))
        current_count = len(self.messages)
        logger_memory.info(f"AI message added. Current message count: {current_count}")
        self._truncate()
        
    def _truncate(self):
        """Keep only recent messages to avoid context bloat"""
        if len(self.messages) > self.max_messages:
            removed_count = len(self.messages) - self.max_messages
            self.messages = self.messages[-self.max_messages:]
            logger_memory.info(f"Memory truncated: removed {removed_count} oldest messages, keeping {len(self.messages)} most recent")
        else:
            logger_memory.debug(f"No truncation needed. Current count: {len(self.messages)}, max: {self.max_messages}")
            
    def get_history(self) -> List:
        """Get formatted conversation history"""
        history = self.messages
        logger_memory.debug(f"Retrieving history: {len(history)} messages")
        return history
    
    def get_history_text(self) -> str:
        """Get history as formatted text"""
        if not self.messages:
            logger_memory.debug("No conversation history available")
            return "No previous conversation"
        
        history_text = []
        for msg in self.messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            history_text.append(f"{role}: {msg.content}")
        
        formatted = "\n".join(history_text)
        logger_memory.debug(f"Formatted history: {len(formatted)} characters, {len(self.messages)} messages")
        return formatted
