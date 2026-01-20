---
title: Context Engineering Visualizer
emoji: 🧠
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: 6.3.0
app_file: main.py
pinned: false
license: mit
short_description: Visualize AI agent context window information flow
tags:
  - langchain
  - context-engineering
  - rag
  - educational
  - visualization
---

# Context Engineering Visualizer

A professional educational tool that demonstrates how information flows into an AI agent's context window before inference. Built with LangChain and Gradio.

Application deployed on Hugging Face: [Context Engineering Visualizer](https://huggingface.co/spaces/mcikalmerdeka/context-engineering-visualizer)

## What Is Context Engineering?

> **Context engineering is the practice of deliberately deciding what information an AI model sees, when it sees it, and in what format.**

Most developers only focus on prompt engineering (optimizing the wording of queries). But the real power comes from **context engineering**: designing the entire information flow into your model.

### Context Engineering vs. Prompt Engineering

| Aspect             | Prompt Engineering | Context Engineering       |
| ------------------ | ------------------ | ------------------------- |
| **Focus**    | Wording            | Information flow          |
| **Scope**    | Single message     | Entire system             |
| **Strategy** | Optimize phrasing  | Optimize context assembly |
| **Tools**    | Text tricks        | RAG, memory, tools        |

Think of it this way:

> **Prompt engineering shapes how you ask. Context engineering shapes what the model understands.**

## What Goes Into "Context"?

When you call an LLM, you're not just sending a prompt. You're sending a **multi-layered context window**:

1. **System Instructions**: Stable behavioral guidelines
2. **Conversation History**: Recent interactions for continuity
3. **Retrieved Knowledge (RAG)**: Relevant documents from a knowledge base
4. **User Query**: The current question or request
5. **Available Tools**: External functions the agent can use

Most developers only optimize layer #4 (the user query). **Context engineering optimizes all five layers.**

## The Four Principles of Context Engineering

### 1. Relevance: Only Include What Helps

```python
# Bad: Dump everything
docs = vectorstore.get_all_documents()  # 1000+ docs, 50k tokens

# Good: Retrieve top-k relevant
docs = retriever.invoke(query, k=2)  # 2 docs, ~100 tokens
```

More context ≠ better answers. Noise hurts performance and costs money.

### 2. Structure: Organize Information Clearly

```python
# Bad: Mix everything together
context = f"{system_prompt} {docs} {history} {query} {tools}"

# Good: Clear layers
context = f"""System Instructions:
{system_prompt}

Conversation History:
{history}

Retrieved Knowledge:
{docs}

Current Question:
{query}"""
```

Models perform better when they can distinguish between different types of information.

### 3. Timing: Retrieve Information When Needed

```python
# Bad: Pre-load everything
def __init__(self):
    self.all_docs = load_entire_database()  # Loaded once
  
# Good: Dynamic retrieval
def process_query(self, query: str):
    docs = self.retriever.invoke(query)  # Retrieved per-query
```

Don't front-load information. Fetch what you need, when you need it.

### 4. Consistency: Use Stable Patterns

```python
# Stable system prompt
self.system_prompt = "You are a data analyst assistant..."

# Predictable temperature
self.llm = ChatOpenAI(model="gpt-4.1-mini", temperature=0)

# Reusable context assembly
def assemble_context(self, query):
    return {
        "system": self.system_prompt,
        "history": self.memory.get_recent(n=4),
        "knowledge": self.retrieve(query, k=2),
        "query": query
    }
```

Consistency reduces randomness and improves reliability.

## Features

This visualizer demonstrates all four principles in action:

- **Interactive Chat Interface**: Clean, modern chatbot UI with conversation history
- **Visual Context Breakdown**: Custom stacked container visualization showing proportional token distribution
- **Advanced RAG Integration**: FAISS vector store with PDF document processing and optimized chunking strategy
- **Conversation Memory**: Smart truncation of conversation history
- **Specialized Tool System**: Metric calculation tools that defer to centralized computation logic
- **Real-time Token Tracking**: See exactly how tokens are distributed across context layers
- **Metadata Display**: Retrieved chunks include source page information for traceability
- **Collapsible Sidebar**: Settings and example questions in an easy-to-access sidebar

## Project Structure

```
context-engineering-visualizer/
├── app/
│   ├── __init__.py
│   ├── agent.py               # Main agent implementation
│   ├── visualizer.py          # Context visualization logic
│   ├── memory.py              # Conversation memory management
│   ├── knowledge.py           # RAG knowledge base with FAISS
│   ├── tools.py               # Agent tools (metric calculations)
│   ├── ui.py                  # Gradio interface
│   └── process_knowledge.py   # Script to create FAISS index
├── config/
│   ├── __init__.py
│   └── settings.py            # Application configuration
├── data/
│   └── Product Strategy & Decision Handbook — Atlas Pay.pdf
├── faiss_index_store/         # Generated FAISS vector store (gitignored)
├── main.py                    # Entry point
├── pyproject.toml
└── README.md
```

## Installation

1. Clone the repository:

```bash
git clone https://github.com/mcikalmerdeka/context-engineering-visualizer
cd context-engineering-visualizer
```

2. Install dependencies using uv:

```bash
uv sync
```

3. Create a `.env` file with your OpenAI API key:

```
OPENAI_API_KEY=your_api_key_here
```

4. Process the PDF and create the FAISS index:

```bash
python app/process_knowledge.py
```

This will:
- Load the Product Strategy PDF document
- Split it into optimized chunks (800 chars with 150 char overlap)
- Create embeddings using OpenAI `text-embedding-3-small`
- Save the FAISS index to `faiss_index_store/`
- Display all chunks with metadata and statistics

## Usage

Run the Gradio application:

```bash
python main.py
```

The interface will launch at `http://127.0.0.1:7860`

## Interface Overview

The Gradio interface features:

1. **Collapsible Sidebar**: Contains settings and sequential example questions organized by scenario
2. **Chat Interface**: Main conversation area with user messages on the right, assistant on the left
3. **Context Window Breakdown**: Visual stacked container showing proportional token distribution
4. **Detailed Layer Contents**: Expandable section with full content of each context layer

### Visual Context Breakdown

The visualizer uses a custom stacked container visualization (similar to a database cylinder) where each layer's height is proportional to its token usage. When you ask a question, you'll see:

- **System Instructions** (Blue): Stable behavioral guidelines
- **Conversation History** (Purple): Recent messages for context
- **Retrieved Knowledge** (Green): Relevant documents from RAG
- **User Query** (Orange): Your current question
- **Available Tools** (Red): Functions the agent can call

Each section displays:

- Layer name and purpose
- Token count and percentage
- Proportional visual representation

Notice what's happening:

- Only **2 relevant documents** retrieved (not the entire knowledge base)
- **Clear separation** between instructions, data, and query
- **Token-efficient** design
- **Tools available** but only called when needed

The model receives exactly what it needs, no more, no less.

### Scenario Examples

The interface includes five sequential scenarios in the sidebar demonstrating an **internal company knowledge assistant** for AtlasPay:

**Scenario 1: Understanding STAM (North Star Metric)**

1. What is STAM and why is it our North Star metric?
2. Calculate STAM if we have 125,000 successful transactions and 500 active merchants
3. What does this STAM value tell us about merchant engagement?

**Scenario 2: Net Revenue Retention Analysis**

1. What is Net Revenue Retention (NRR) and why is it important?
2. Calculate NRR if we have $2.5M retained revenue from $2M starting revenue
3. Is this NRR performance good based on our product goals?

**Scenario 3: Payment Success Rate Monitoring**

1. What is Adjusted Payment Success Rate and how is it used?
2. Calculate the payment success rate with 48,500 successful payments out of 50,000 valid attempts
3. Does this meet our platform reliability standards?

**Scenario 4: Product Strategy & Decision Making**

1. What are AtlasPay's core product principles?
2. Why did we decide to build our fraud detection in-house instead of buying a vendor solution?
3. What were the trade-offs in that decision?

**Scenario 5: Feature Prioritization**

1. How does AtlasPay prioritize features?
2. What are our strategic goals for 2025-2027?
3. Should we prioritize a feature with Customer Impact=5, Revenue Impact=4, Strategic Alignment=5, Engineering Effort=3?

These scenarios demonstrate:

- **Advanced RAG retrieval**: Semantic search over product strategy documentation
- **Specialized tool usage**: Metric calculations using centralized computation logic
- **Context awareness**: Using conversation history for follow-up questions
- **Source traceability**: Retrieved chunks include page metadata

### Key Insight: Document Structure vs. Computation Logic

The Product Strategy Handbook **intentionally omits calculation formulas** for metrics like STAM, NRR, and Payment Success Rate. Instead, it references the "official metrics service" or "centralized metrics system."

This design pattern demonstrates:

1. **Separation of concerns**: Documentation describes *what* and *why*, not *how*
2. **Single source of truth**: Formulas live in one place (the tool), preventing drift
3. **Tool dependency**: The agent must call `calculate_metric` tool for computations
4. **Real-world modeling**: Mirrors how actual organizations structure their knowledge

The third question in each scenario showcases context engineering - the agent understands follow-ups because we engineered the context to include relevant history and retrieved documentation.

## Using the Interface

1. **Open the sidebar** to see settings and example questions
2. **Enable/disable context visualization** using the checkbox
3. **Follow the sequential scenarios** to understand how context engineering works
4. **Ask your own questions** about business metrics
5. **Expand the Context Window Breakdown** to see the visual token distribution
6. **View detailed layer contents** by expanding the nested accordion

The interface is designed to be educational - each interaction shows you exactly how the context is assembled before being sent to the model.

## Common Context Engineering Mistakes

### Mistake 1: Dumping Entire Documents

```python
# Don't do this
context = "\n".join(all_documents)  # 50,000 tokens
```

**Fix:** Use semantic search to retrieve only top-k relevant chunks.

### Mistake 2: Sending Full Chat History

```python
# Don't do this
history = self.all_messages  # Entire conversation since session start
```

**Fix:** Smart truncation (last N messages) or summarization.

### Mistake 3: Mixing Instructions with Data

```python
# Don't do this
prompt = f"You're a helpful assistant. Here's data: {data}. User asks: {query}"
```

**Fix:** Separate system instructions, data, and query into distinct layers.

### Mistake 4: Static Context

```python
# Don't do this
self.context = load_all_context()  # Loaded once, used forever
```

**Fix:** Assemble context dynamically per query.

### Mistake 5: Ignoring Token Costs

```python
# Don't do this
# (No awareness of context size or cost)
```

**Fix:** Track token counts per layer. Visualize distribution. Optimize.

## Code Architecture

### The Agent

The main agent assembles context layer by layer:

```python
class ContextEngineeringAgent:
    def process_query(self, user_query: str):
        # Layer 1: System instructions (stable)
        # Layer 2: Conversation history (recent only)
        history_text = self.memory.get_history_text()
    
        # Layer 3: Retrieved knowledge (top-2 relevant)
        retrieved_docs = self.knowledge_base.retrieve_relevant(user_query)
    
        # Layer 4: User query
        # Layer 5: Tools (automatically handled by agent)
    
        # Assemble with clear structure
        context_message = f"""Context from Knowledge Base:
{retrieved_docs}

Previous Conversation:
{history_text}

Current Question:
{user_query}"""
    
        return self.agent.invoke({"messages": [{"role": "user", "content": context_message}]})
```

### The RAG Component (Relevance in Action)

```python
class KnowledgeBase:
    def __init__(self, pdf_path: str, index_path: str, embedding_model: str, top_k: int = 3):
        self.embeddings = OpenAIEmbeddings(model=embedding_model)
        self.vectorstore = self._load_or_create_index(recreate=False)
        self.top_k = top_k
    
    def _load_or_create_index(self, recreate: bool = False) -> FAISS:
        # Load existing index or create from PDF
        if not recreate and os.path.exists(self.index_path):
            return FAISS.load_local(self.index_path, self.embeddings)
        
        # Load PDF and split into chunks
        loader = PyPDFLoader(self.pdf_path)
        documents = loader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=800,      # Optimized for structured content
            chunk_overlap=150,   # Balance between context and redundancy
            separators=["\n\n", "\n", ". ", ", ", " ", ""]
        )
        chunks = text_splitter.split_documents(documents)
        
        # Create and save FAISS index
        vectorstore = FAISS.from_documents(chunks, self.embeddings)
        vectorstore.save_local(self.index_path)
        return vectorstore
    
    def retrieve_relevant(self, query: str, k: int = None) -> str:
        """Retrieve top-k relevant chunks with metadata"""
        docs = self.vectorstore.similarity_search(query, k=k or self.top_k)
        
        formatted_chunks = []
        for i, doc in enumerate(docs, 1):
            chunk_text = f"--- Chunk {i} ---\nMetadata: {doc.metadata}\n\n{doc.page_content}"
            formatted_chunks.append(chunk_text)
        
        return "\n\n".join(formatted_chunks)
```

**Key RAG optimizations:**

1. **Persistent index**: FAISS index saved to disk, loaded on startup (no re-embedding)
2. **Smart chunking**: 800 char chunks with 150 overlap balances granularity and context
3. **Separator hierarchy**: Respects paragraph > sentence > clause boundaries
4. **Top-k retrieval**: Only 3 most relevant chunks (not entire document)
5. **Metadata tracking**: Each chunk includes source page for traceability

We process a 10+ page PDF into ~50 chunks, but only send the **top 3 most relevant** to the model. This is context engineering in action.

### The Memory Component (Smart Truncation)

```python
class ConversationMemory:
    def __init__(self, max_messages: int = 4):
        self.messages = []
        self.max_messages = max_messages
  
    def _truncate(self):
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
```

We limit history to 4 messages. For longer conversations, this prevents context overflow while maintaining relevant continuity.

**Note:** There are several approaches to handle conversation history when it becomes too long:

- **Trimming**: Keep only the most recent N messages (used here)
- **Summarization**: Compress older messages into summaries
- **Deletion**: Permanently remove certain states
- More info: [LangChain Memory Documentation](https://docs.langchain.com/oss/python/concepts/memory)

### The Tool System (Specialized Computation)

```python
@tool
def calculate_metric(metric_name: str, values: str) -> str:
    """
    Compute an official business metric using centralized metrics logic.
    
    This tool represents the company's authoritative metrics service.
    Product strategy documents intentionally omit calculation formulas
    and defer all computations to this tool to ensure consistency.
    
    Supported metrics:
    - "stam": Successful Transactions per Active Merchant
    - "nrr": Net Revenue Retention
    - "payment_success_rate": Adjusted Payment Success Rate
    
    Args:
        metric_name: Name of the metric to compute
        values: Comma-separated numeric inputs (e.g., "125000, 500")
    
    Returns:
        Human-readable string with computed metric
    """
    nums = [float(x.strip()) for x in values.split(",")]
    
    if metric_name.lower() == "stam":
        result = nums[0] / nums[1]  # transactions / merchants
        return f"STAM: {result:.2f} successful transactions per merchant"
    
    elif metric_name.lower() == "nrr":
        result = (nums[0] / nums[1]) * 100  # retained / starting
        return f"Net Revenue Retention (NRR): {result:.2f}%"
    
    # ... other metrics
```

**Design pattern:**

- **Documentation separation**: PDF describes metrics conceptually, not computationally
- **Single source of truth**: Formulas exist only in the tool
- **Forced tool usage**: Agent cannot compute metrics from context alone
- **Real-world modeling**: Mimics actual enterprise metric systems

This ensures:
1. **Consistency**: All metric calculations use same logic
2. **Maintainability**: Formula changes update in one place
3. **Auditability**: Tool calls are traceable
4. **No hallucination**: Agent can't make up formulas

## Configuration

Edit `config/settings.py` to customize:

```python
class Settings:
    # Model settings
    MODEL_NAME = "gpt-4.1-mini"
    TEMPERATURE = 0
    EMBEDDING_MODEL = "text-embedding-3-small"
  
    # Memory settings
    MAX_CONVERSATION_MESSAGES = 4
  
    # RAG settings
    RAG_TOP_K = 3
    FAISS_INDEX_PATH = "faiss_index_store"
    PDF_PATH = "data/Product Strategy & Decision Handbook — Atlas Pay.pdf"
  
    # UI settings
    GRADIO_SERVER_PORT = 7860
    
    # System prompt
    SYSTEM_PROMPT = """You are an internal company knowledge assistant for AtlasPay..."""
```

## How to Practice Context Engineering

### 1. Inspect Your Token Usage

```python
def count_tokens(text: str) -> int:
    # Simple estimate: ~4 chars per token
    return len(text) // 4

print(f"Context size: {count_tokens(context)} tokens")
```

### 2. Separate Concerns

```python
# Instead of one blob, create layers
context = {
    "system": system_instructions,
    "history": recent_messages,
    "knowledge": retrieved_docs,
    "query": user_question
}
```

### 3. Experiment with Context Size

```python
# Try different values
retriever = vectorstore.as_retriever(search_kwargs={"k": k})
# Test k=1, k=2, k=5, k=10
# Measure: quality vs. cost vs. latency
```

### 4. Treat Context as First-Class

Don't think of context as "everything I stuff into the prompt." Think of it as a carefully engineered data pipeline with:

- **Sources** (RAG, memory, tools)
- **Filters** (relevance, recency, size)
- **Transformations** (formatting, structuring)
- **Quality checks** (token budgets, validation)

## Key Takeaways

1. **Context is multi-layered**: It's not just your prompt
2. **Less is often more**: Relevant beats comprehensive
3. **Structure matters**: Organization helps models reason
4. **Dynamic beats static**: Assemble context per-query
5. **Tokens cost money**: Engineering context saves budget

## Why This Matters

As AI systems mature, **context design is becoming the main differentiator**:

1. **Larger context windows ≠ free intelligence**: A 1M token context window doesn't mean you should use it all
2. **AI agents depend on state & memory**: Poor context management = inconsistent behavior
3. **Cost optimization is critical**: Every token costs money
4. **Reliability > raw capability**: A GPT-3.5 with good context beats GPT-4 with bad context

## Technologies

- **LangChain**: Agent framework, tools, and document processing
- **OpenAI**: Language model (GPT-4.1-mini) and embeddings (text-embedding-3-small)
- **FAISS**: Vector store for semantic search and RAG
- **PyPDF**: PDF document loading and parsing
- **Gradio**: Web interface
- **Python 3.11+**

## Contributing

This is an educational project designed to help developers understand context engineering. Feel free to:

- Open issues for bugs or suggestions
- Submit pull requests for improvements
- Use this as a learning resource for your own projects
