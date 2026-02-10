"""Main agent implementation"""

from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from .visualizer import ContextVisualizer
from .memory import ConversationMemory
from .knowledge import KnowledgeBase
from .tools import calculate_metric, get_current_time
from config.settings import Settings
from config import logger_agent, logger_memory, logger_knowledge


class ContextEngineeringAgent:
    """
    Agent that demonstrates context engineering principles:
    - Relevance: Only includes needed context
    - Structure: Clear separation of context layers
    - Timing: Retrieves information when needed
    - Consistency: Stable system instructions
    """
    
    def __init__(self):
        logger_agent.info("Initializing ContextEngineeringAgent")
        
        # Initialize components
        logger_agent.debug(f"Initializing LLM with model: {Settings.MODEL_NAME}")
        self.llm = ChatOpenAI(
            model=Settings.MODEL_NAME,
            temperature=Settings.TEMPERATURE
        )
        
        logger_agent.info("Loading knowledge base from FAISS index")
        self.knowledge_base = KnowledgeBase(
            pdf_path=Settings.PDF_PATH,
            index_path=Settings.FAISS_INDEX_PATH,
            embedding_model=Settings.EMBEDDING_MODEL,
            top_k=Settings.RAG_TOP_K,
            recreate_index=False  # Load existing index by default
        )
        
        logger_agent.debug(f"Initializing conversation memory (max_messages={Settings.MAX_CONVERSATION_MESSAGES})")
        self.memory = ConversationMemory(max_messages=Settings.MAX_CONVERSATION_MESSAGES)
        self.visualizer = ContextVisualizer()
        
        # System instructions
        self.system_prompt = Settings.SYSTEM_PROMPT
        
        # Create tools
        self.tools = [calculate_metric, get_current_time]
        logger_agent.debug(f"Created {len(self.tools)} tools: {[t.name for t in self.tools]}")
        
        # Create agent
        logger_agent.info("Creating LangChain agent with system prompt and tools")
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
        
        logger_agent.info("ContextEngineeringAgent initialized successfully")
        
    def process_query(self, user_query: str) -> tuple[str, ContextVisualizer]:
        """
        Process a user query with full context engineering
        Returns: (response, visualizer)
        """
        logger_agent.info(f"Processing query: {user_query[:50]}..." if len(user_query) > 50 else f"Processing query: {user_query}")
        
        # Reset visualizer for new query
        self.visualizer = ContextVisualizer()
        
        # Layer 1: System Instructions
        logger_agent.debug("Adding layer: System Instructions")
        self.visualizer.add_layer(
            "System Instructions",
            self.system_prompt,
        )
        
        # Layer 2: Conversation History
        logger_memory.debug("Retrieving conversation history")
        history_text = self.memory.get_history_text()
        logger_agent.debug(f"Conversation history length: {len(history_text)} characters")
        self.visualizer.add_layer(
            "Conversation History",
            history_text if history_text != "No previous conversation" else "No previous conversation",
        )
        
        # Layer 3: Retrieved Knowledge (RAG)
        logger_knowledge.info(f"Retrieving relevant documents for query")
        retrieved_context = self.knowledge_base.retrieve_relevant(user_query)
        doc_count = len([c for c in retrieved_context.split("--- Chunk") if c.strip()])
        logger_knowledge.info(f"Retrieved {doc_count} document chunks")
        logger_agent.debug(f"Retrieved context length: {len(retrieved_context)} characters")
        self.visualizer.add_layer(
            "Retrieved Knowledge (RAG)",
            retrieved_context,
        )
        
        # Layer 4: Current User Query
        logger_agent.debug("Adding layer: User Query")
        self.visualizer.add_layer(
            "User Query",
            user_query,
        )
        
        # Layer 5: Available Tools
        logger_agent.debug("Adding layer: Available Tools")
        tools_context = "\n".join([
            f"- {tool.name}: {tool.description}" for tool in self.tools
        ])
        self.visualizer.add_layer(
            "Available Tools",
            tools_context,
        )
        
        # Build the context structure
        total_tokens = sum(self.visualizer.token_counts.values())
        logger_agent.info(f"Total context size: {total_tokens} tokens across {len(self.visualizer.context_layers)} layers")
        
        context_message = f"""Context from Knowledge Base:
{retrieved_context}

Previous Conversation:
{history_text}

Current Question:
{user_query}"""
        
        # Invoke agent
        logger_agent.info("Invoking LangChain agent with assembled context")
        try:
            result = self.agent.invoke({
                "messages": [{"role": "user", "content": context_message}]
            })
            logger_agent.info("Agent invocation successful")
        except Exception as e:
            logger_agent.error(f"Agent invocation failed: {str(e)}")
            raise
        
        # Extract response
        response = result["messages"][-1].content
        response_preview = response[:100] + "..." if len(response) > 100 else response
        logger_agent.info(f"Generated response: {response_preview}")
        
        # Update conversation memory
        logger_memory.info("Adding user message to conversation memory")
        self.memory.add_user_message(user_query)
        logger_memory.info("Adding AI response to conversation memory")
        self.memory.add_ai_message(response)
        
        logger_agent.info("Query processing completed successfully")
        return response, self.visualizer
