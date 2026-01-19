"""Knowledge base with RAG capabilities"""

from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS


class KnowledgeBase:
    """Simulates a knowledge base with RAG capabilities"""
    
    def __init__(self, top_k: int = 2):
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
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": top_k})
        
    def retrieve_relevant(self, query: str) -> str:
        """Retrieve relevant documents for a query"""
        docs = self.retriever.invoke(query)
        return "\n".join([f"- {doc.page_content}" for doc in docs])
