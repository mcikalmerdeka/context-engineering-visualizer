"""Conversation memory management"""

from typing import List
from langchain.messages import HumanMessage, AIMessage


class ConversationMemory:
    """Manages conversation history with smart truncation"""
    
    def __init__(self, max_messages: int = 4):
        self.messages = []
        self.max_messages = max_messages
        
    def add_user_message(self, content: str):
        """Add user message to history"""
        self.messages.append(HumanMessage(content=content))
        self._truncate()
        
    def add_ai_message(self, content: str):
        """Add AI message to history"""
        self.messages.append(AIMessage(content=content))
        self._truncate()
        
    def _truncate(self):
        """Keep only recent messages to avoid context bloat"""
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
            
    def get_history(self) -> List:
        """Get formatted conversation history"""
        return self.messages
    
    def get_history_text(self) -> str:
        """Get history as formatted text"""
        if not self.messages:
            return "No previous conversation"
        
        history_text = []
        for msg in self.messages:
            role = "User" if isinstance(msg, HumanMessage) else "Assistant"
            history_text.append(f"{role}: {msg.content}")
        return "\n".join(history_text)
