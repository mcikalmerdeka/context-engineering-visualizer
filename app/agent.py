"""Main agent implementation"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from .visualizer import ContextVisualizer
from .memory import ConversationMemory
from .knowledge import KnowledgeBase
from .tools import calculate_metric, get_current_time
from config import Settings


class ContextEngineeringAgent:
    """
    Agent that demonstrates context engineering principles:
    - Relevance: Only includes needed context
    - Structure: Clear separation of context layers
    - Timing: Retrieves information when needed
    - Consistency: Stable system instructions
    """
    
    def __init__(self):
        # Initialize components
        self.llm = ChatOpenAI(
            model=Settings.MODEL_NAME,
            temperature=Settings.TEMPERATURE
        )
        
        self.knowledge_base = KnowledgeBase(top_k=Settings.RAG_TOP_K)
        self.memory = ConversationMemory(max_messages=Settings.MAX_CONVERSATION_MESSAGES)
        self.visualizer = ContextVisualizer()
        
        # System instructions
        self.system_prompt = Settings.SYSTEM_PROMPT
        
        # Create tools
        self.tools = [calculate_metric, get_current_time]
        
        # Create agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
        
    def process_query(self, user_query: str) -> tuple[str, ContextVisualizer]:
        """
        Process a user query with full context engineering
        Returns: (response, visualizer)
        """
        # Reset visualizer for new query
        self.visualizer = ContextVisualizer()
        
        # Layer 1: System Instructions
        self.visualizer.add_layer(
            "System Instructions",
            self.system_prompt,
        )
        
        # Layer 2: Conversation History
        history_text = self.memory.get_history_text()
        self.visualizer.add_layer(
            "Conversation History",
            history_text if history_text != "No previous conversation" else "No previous conversation",
        )
        
        # Layer 3: Retrieved Knowledge (RAG)
        retrieved_context = self.knowledge_base.retrieve_relevant(user_query)
        self.visualizer.add_layer(
            "Retrieved Knowledge (RAG)",
            retrieved_context,
        )
        
        # Layer 4: Current User Query
        self.visualizer.add_layer(
            "User Query",
            user_query,
        )
        
        # Layer 5: Available Tools
        tools_context = "\n".join([
            f"- {tool.name}: {tool.description}" for tool in self.tools
        ])
        self.visualizer.add_layer(
            "Available Tools",
            tools_context,
        )
        
        # Build the context structure
        context_message = f"""Context from Knowledge Base:
{retrieved_context}

Previous Conversation:
{history_text}

Current Question:
{user_query}"""
        
        # Invoke agent
        result = self.agent.invoke({
            "messages": [{"role": "user", "content": context_message}]
        })
        
        # Extract response
        response = result["messages"][-1].content
        
        # Update conversation memory
        self.memory.add_user_message(user_query)
        self.memory.add_ai_message(response)
        
        return response, self.visualizer
