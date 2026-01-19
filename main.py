"""
Context Engineering Visualizer
Demonstrates how information flows into an agent's context window before inference
"""

import os
from typing import List, Dict, Any
from datetime import datetime
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.agents import create_agent
from langchain.tools import tool
from langchain.messages import HumanMessage, AIMessage
from langchain_community.vectorstores import FAISS

# Load environment variables
load_dotenv()

# ============================================
# CONTEXT ENGINEERING COMPONENTS
# ============================================

class ContextVisualizer:
    """Tracks and visualizes what goes into the context window"""
    
    def __init__(self):
        self.context_layers = []
        self.token_counts = {}
        
    def add_layer(self, layer_name: str, content: str, token_estimate: int = None):
        """Add a context layer for visualization"""
        if token_estimate is None:
            # Rough estimate: ~4 chars per token
            token_estimate = len(content) // 4
            
        self.context_layers.append({
            "layer": layer_name,
            "content": content,
            "tokens": token_estimate,
            "timestamp": datetime.now().isoformat()
        })
        self.token_counts[layer_name] = token_estimate
        
    def visualize(self):
        """Display the context window structure"""
        print("\n" + "="*80)
        print("CONTEXT WINDOW VISUALIZATION")
        print("="*80)
        
        total_tokens = sum(self.token_counts.values())
        
        for i, layer in enumerate(self.context_layers, 1):
            percentage = (layer["tokens"] / total_tokens * 100) if total_tokens > 0 else 0
            bar_length = int(percentage / 2)
            bar = "█" * bar_length
            
            print(f"\n{i}. {layer['layer'].upper()}")
            print(f"   Tokens: {layer['tokens']} ({percentage:.1f}%)")
            print(f"   [{bar:<50}]")
            print(f"   Content:\n{layer['content']}")
            
        print(f"\n{'='*80}")
        print(f"TOTAL CONTEXT TOKENS: {total_tokens}")
        print(f"{'='*80}\n")
        
    def get_summary(self) -> Dict[str, Any]:
        """Get structured summary of context"""
        return {
            "layers": [l["layer"] for l in self.context_layers],
            "total_tokens": sum(self.token_counts.values()),
            "breakdown": self.token_counts
        }


# ============================================
# KNOWLEDGE BASE (RAG Component)
# ============================================

class KnowledgeBase:
    """Simulates a knowledge base with RAG capabilities"""
    
    def __init__(self):
        # Sample knowledge documents about data analytics
        self.documents = [
            "Gross Revenue is defined as total sales before refunds and returns.",
            "Net Revenue equals gross revenue minus refunds, returns, and discounts.",
            "AOV (Average Order Value) is calculated as total revenue divided by number of orders.",
            "Customer Lifetime Value (CLV) is the total revenue expected from a customer over their entire relationship.",
            "Conversion Rate is the percentage of visitors who complete a desired action.",
            "Churn Rate measures the percentage of customers who stop using your service over a period.",
            "Monthly Recurring Revenue (MRR) is the predictable revenue generated each month.",
            "CAC (Customer Acquisition Cost) is the total cost of acquiring a new customer.",
        ]
        
        # Create embeddings and vector store
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = FAISS.from_texts(self.documents, self.embeddings)
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": 2})
        
    def retrieve_relevant(self, query: str) -> str:
        """Retrieve relevant documents for a query"""
        docs = self.retriever.invoke(query)
        return "\n".join([f"- {doc.page_content}" for doc in docs])


# ============================================
# CONVERSATION MEMORY
# ============================================

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
            # Keep the most recent messages
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


# ============================================
# TOOLS (External Connections)
# ============================================

@tool
def calculate_metric(
    metric_name: str,
    values: str
) -> str:
    """
    Calculate a business metric.
    
    Args:
        metric_name: Name of metric (aov, conversion_rate, clv, etc.)
        values: Comma-separated values needed for calculation
    """
    try:
        nums = [float(x.strip()) for x in values.split(",")]
        
        if metric_name.lower() == "aov":
            # Average Order Value = total revenue / number of orders
            if len(nums) >= 2:
                result = nums[0] / nums[1]
                return f"AOV: ${result:.2f}"
                
        elif metric_name.lower() == "conversion_rate":
            # Conversion Rate = (conversions / visitors) * 100
            if len(nums) >= 2:
                result = (nums[0] / nums[1]) * 100
                return f"Conversion Rate: {result:.2f}%"
                
        elif metric_name.lower() == "churn_rate":
            # Churn Rate = (customers lost / total customers) * 100
            if len(nums) >= 2:
                result = (nums[0] / nums[1]) * 100
                return f"Churn Rate: {result:.2f}%"
                
        return f"Calculated {metric_name} with values {values}"
        
    except Exception as e:
        return f"Error calculating metric: {str(e)}"


@tool
def get_current_time() -> str:
    """Get the current date and time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ============================================
# CONTEXT ENGINEERING AGENT
# ============================================

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
            model="gpt-4.1-mini",
            temperature=0  # Low temp for consistency
        )
        
        self.knowledge_base = KnowledgeBase()
        self.memory = ConversationMemory(max_messages=4)
        self.visualizer = ContextVisualizer()
        
        # System instructions (STABLE CONTEXT)
        self.system_prompt = """You are a data analyst assistant.

Your role:
- Answer questions about business metrics and data analysis
- Use the provided context and knowledge to give accurate answers
- If context is insufficient, clearly state what information is missing
- Always explain your reasoning briefly
- Use the calculator tool for numeric computations

Be concise, accurate, and helpful."""
        
        # Create tools
        self.tools = [calculate_metric, get_current_time]
        
        # Create agent
        self.agent = create_agent(
            model=self.llm,
            tools=self.tools,
            system_prompt=self.system_prompt
        )
        
    def process_query(self, user_query: str, show_visualization: bool = True) -> str:
        """
        Process a user query with full context engineering visualization
        """
        # Reset visualizer for new query
        self.visualizer = ContextVisualizer()
        
        print(f"\n{'='*80}")
        print(f"USER QUERY: {user_query}")
        print(f"{'='*80}\n")
        
        # ============================================
        # LAYER 1: System Instructions
        # ============================================
        self.visualizer.add_layer(
            "System Instructions",
            self.system_prompt,
        )
        
        # ============================================
        # LAYER 2: Conversation History
        # ============================================
        history_text = self.memory.get_history_text()
        self.visualizer.add_layer(
            "Conversation History",
            history_text if history_text != "No previous conversation" else "No previous conversation",
        )
        
        # ============================================
        # LAYER 3: Retrieved Knowledge (RAG)
        # ============================================
        retrieved_context = self.knowledge_base.retrieve_relevant(user_query)
        self.visualizer.add_layer(
            "Retrieved Knowledge (RAG)",
            retrieved_context,
        )
        
        # ============================================
        # LAYER 4: Current User Query
        # ============================================
        self.visualizer.add_layer(
            "User Query",
            user_query,
        )
        
        # ============================================
        # LAYER 5: Available Tools
        # ============================================
        tools_context = "\n".join([
            f"- {tool.name}: {tool.description}" for tool in self.tools
        ])
        self.visualizer.add_layer(
            "Available Tools",
            tools_context,
        )
        
        # Show visualization BEFORE inference
        if show_visualization:
            self.visualizer.visualize()
            print("\n🤖 Sending context to model for inference...\n")
        
        # ============================================
        # INFERENCE: Agent processes with full context
        # ============================================
        
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
        
        # Show response
        print(f"\n{'='*80}")
        print("AGENT RESPONSE:")
        print(f"{'='*80}")
        print(response)
        print(f"{'='*80}\n")
        
        return response


# ============================================
# DEMO SCENARIOS
# ============================================

def run_demo():
    """Run demonstration scenarios"""
    
    print("\n" + "🎯" * 40)
    print("CONTEXT ENGINEERING VISUALIZER")
    print("Demonstrates how information flows into an agent's context window")
    print("🎯" * 40)
    
    agent = ContextEngineeringAgent()
    
    # Scenario 1: Simple query with RAG
    print("\n\n" + "📊 SCENARIO 1: RAG-based Query" + "\n")
    agent.process_query(
        "What is Average Order Value and how is it calculated?"
    )
    
    input("\n⏸️  Press Enter to continue to next scenario...")
    
    # Scenario 2: Query with tool use
    print("\n\n" + "🔧 SCENARIO 2: Query Requiring Tool Use" + "\n")
    agent.process_query(
        "Calculate the AOV if total revenue is $50000 and we had 500 orders"
    )
    
    input("\n⏸️  Press Enter to continue to next scenario...")
    
    # Scenario 3: Query with conversation history
    print("\n\n" + "💬 SCENARIO 3: Query Using Conversation Context" + "\n")
    agent.process_query(
        "What about if we had 750 orders instead?"
    )
    
    input("\n⏸️  Press Enter to see context summary...")
    
    # Show final summary
    print("\n\n" + "📈 CONTEXT ENGINEERING SUMMARY" + "\n")
    summary = agent.visualizer.get_summary()
    print(f"Context Layers Used: {', '.join(summary['layers'])}")
    print(f"Total Context Tokens: {summary['total_tokens']}")
    print(f"\nToken Breakdown:")
    for layer, tokens in summary['breakdown'].items():
        print(f"  - {layer}: {tokens} tokens")


# ============================================
# INTERACTIVE MODE
# ============================================

def run_interactive():
    """Run interactive mode"""
    
    print("\n" + "💡" * 40)
    print("CONTEXT ENGINEERING - INTERACTIVE MODE")
    print("💡" * 40)
    print("\nType your questions. Type 'quit' to exit.\n")
    
    agent = ContextEngineeringAgent()
    
    while True:
        try:
            user_input = input("\n📝 Your question: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("\n👋 Goodbye!")
                break
                
            if not user_input:
                continue
                
            agent.process_query(user_input, show_visualization=True)
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        run_interactive()
    else:
        run_demo()
