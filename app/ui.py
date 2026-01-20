"""Gradio UI for Context Engineering Visualizer"""

import gradio as gr
from typing import Tuple, List

from .agent import ContextEngineeringAgent
from config import Settings


class ContextVisualizerUI:
    """Gradio interface for the Context Engineering Visualizer"""
    
    def __init__(self):
        self.agent = None
        self.chat_history = []
        
    def initialize_agent(self) -> str:
        """Initialize the agent"""
        try:
            self.agent = ContextEngineeringAgent()
            return "Agent initialized successfully"
        except Exception as e:
            return f"Error initializing agent: {str(e)}"
    
    def format_context_layers(self, visualizer) -> str:
        """Format context layers for display as stacked container visualization"""
        if not visualizer.context_layers:
            return "<div style='text-align: center; padding: 20px;'>No context layers available</div>"
        
        total_tokens = sum(visualizer.token_counts.values())
        
        # Color palette for different layers
        colors = [
            "#4A90E2",  # Blue - System Instructions
            "#7B68EE",  # Purple - Conversation History
            "#50C878",  # Green - Retrieved Knowledge
            "#F39C12",  # Orange - User Query
            "#E74C3C"   # Red - Available Tools
        ]
        
        # Build HTML for stacked container
        html = f"""
        <div style="max-width: 800px; margin: 0 auto; font-family: 'Inter', sans-serif;">
            <div style="text-align: center; margin-bottom: 20px;">
                <h3 style="margin: 0; color: #2c3e50;">Context Window Structure</h3>
                <p style="margin: 5px 0; color: #7f8c8d; font-size: 14px;">Total: {total_tokens} tokens</p>
            </div>
            
            <div style="border: 2px solid #34495e; border-radius: 12px; overflow: hidden; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        """
        
        for i, layer in enumerate(visualizer.context_layers):
            percentage = (layer["tokens"] / total_tokens * 100) if total_tokens > 0 else 0
            color = colors[i % len(colors)]
            
            # Create stacked section
            html += f"""
                <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                            padding: 15px 20px; 
                            border-bottom: 1px solid rgba(255,255,255,0.1);
                            position: relative;
                            height: {max(percentage * 3, 30)}px;
                            display: flex;
                            align-items: center;
                            transition: all 0.3s ease;">
                    <div style="flex: 1;">
                        <div style="color: white; font-weight: 600; font-size: 14px; margin-bottom: 3px;">
                            {layer['layer'].upper()}
                        </div>
                        <div style="color: rgba(255,255,255,0.9); font-size: 12px;">
                            {layer['tokens']} tokens ({percentage:.1f}%)
                        </div>
                    </div>
                    <div style="color: rgba(255,255,255,0.8); font-size: 24px; font-weight: bold;">
                        {percentage:.0f}%
                    </div>
                </div>
            """
        
        html += """
            </div>
        </div>
        """
        
        return html
    
    def format_context_details(self, visualizer) -> str:
        """Format detailed context layer contents for markdown display"""
        if not visualizer.context_layers:
            return "No context layers available"
        
        output = []
        total_tokens = sum(visualizer.token_counts.values())
        
        for i, layer in enumerate(visualizer.context_layers, 1):
            percentage = (layer["tokens"] / total_tokens * 100) if total_tokens > 0 else 0
            
            output.append(f"### {i}. {layer['layer'].upper()}")
            output.append(f"**Tokens:** {layer['tokens']} ({percentage:.1f}%)")
            output.append(f"\n**Content:**")
            output.append(f"```\n{layer['content']}\n```")
            output.append("")
        
        return "\n".join(output)
    
    def format_token_breakdown(self, visualizer) -> List[Tuple[str, int]]:
        """Format token breakdown for chart"""
        if not visualizer.token_counts:
            return []
        
        return [(layer, tokens) for layer, tokens in visualizer.token_counts.items()]
    
    def process_query(
        self, 
        query: str,
        history: List,
        show_visualization: bool
    ) -> Tuple[List, str, str, str]:
        """Process user query and return results"""
        
        if not self.agent:
            self.initialize_agent()
        
        if not query.strip():
            return history, "", "", ""
        
        try:
            # Process query
            response, visualizer = self.agent.process_query(query)
            
            # Add to chat history (format: list of dicts with role and content)
            history.append({"role": "user", "content": query})
            history.append({"role": "assistant", "content": response})
            
            # Format outputs
            if show_visualization:
                context_viz_html = self.format_context_layers(visualizer)
                context_details = self.format_context_details(visualizer)
            else:
                context_viz_html = "<div style='text-align: center; padding: 20px; color: #7f8c8d;'>Visualization disabled</div>"
                context_details = "Visualization disabled"
            
            return history, "", context_viz_html, context_details
            
        except Exception as e:
            error_msg = f"Error processing query: {str(e)}"
            history.append({"role": "user", "content": query})
            history.append({"role": "assistant", "content": error_msg})
            return history, "", "", ""
    
    def clear_conversation(self) -> Tuple[List, str, str]:
        """Clear conversation history"""
        if self.agent:
            self.agent.memory.messages = []
        return [], "", ""
    
    def create_interface(self) -> gr.Blocks:
        """Create the Gradio interface"""
        
        with gr.Blocks(
            title="Context Engineering Visualizer",
            theme=gr.themes.Soft()
        ) as interface:
            
            gr.Markdown("""
            # Context Engineering Visualizer
            
            This tool demonstrates how information flows into an AI agent's context window before inference.
            Ask questions about business metrics and data analysis to see the context engineering in action.
            """)
            
            with gr.Accordion("About Context Engineering", open=False):
                gr.Markdown("""
                **Context Engineering** is the practice of carefully managing what information goes into an AI model's context window.
                
                This visualizer shows five key layers:
                
                1. **System Instructions**: Stable guidelines that define the agent's role and behavior
                2. **Conversation History**: Recent messages to maintain conversational coherence
                3. **Retrieved Knowledge (RAG)**: Relevant information retrieved from a knowledge base
                4. **User Query**: The current question or request
                5. **Available Tools**: External functions the agent can use
                
                Each layer contributes tokens to the context window. Good context engineering ensures:
                - **Relevance**: Only necessary information is included
                - **Structure**: Clear separation and organization of context layers
                - **Efficiency**: Optimal use of limited context window space
                - **Consistency**: Stable system instructions across interactions
                """)
            
            with gr.Sidebar(label="Settings & Examples", open=True, width=320):
                gr.Markdown("### Settings")
                
                show_viz = gr.Checkbox(
                    label="Show Context Visualization",
                    value=True,
                    info="Display detailed breakdown of context layers"
                )
                
                gr.Markdown("### Example Questions")
                gr.Markdown("""
                **Try these sequential scenarios to see context engineering in action:**
                
                **Scenario 1: Understanding AOV (Average Order Value)**
                1. What is Average Order Value and how is it calculated?
                2. Calculate the AOV if total revenue is $50000 and we had 500 orders
                3. What if we had 700 orders with the same revenue instead?
                
                **Scenario 2: Conversion Rate Analysis**
                1. What is Conversion Rate?
                2. Calculate conversion rate with 250 conversions and 10000 visitors
                3. How would the rate change if we got 400 conversions?
                
                **Scenario 3: Understanding Revenue Metrics**
                1. What is the difference between gross and net revenue?
                2. If gross revenue is $100000 with $15000 in refunds and $5000 in discounts, what's the net revenue?
                
                **Scenario 4: Churn Rate**
                1. Explain what Churn Rate means
                2. Calculate churn rate if we lost 50 customers out of 1000 total customers
                """)
            
            chatbot = gr.Chatbot(
                label="Conversation",
                height=500,
                avatar_images=(None, None),
                type='messages'
            )
            
            query_input = gr.Textbox(
                label="Your Question",
                placeholder="e.g., What is Average Order Value and how is it calculated?",
                lines=2,
                show_label=False
            )
            
            with gr.Row():
                submit_btn = gr.Button("Submit", variant="primary")
                clear_btn = gr.Button("Clear Conversation")
            
            with gr.Accordion("Context Window Breakdown", open=True):
                context_viz = gr.HTML(
                    value="<div style='text-align: center; padding: 20px; color: #7f8c8d;'>Submit a query to see context breakdown</div>"
                )
                
                with gr.Accordion("Detailed Layer Contents", open=False):
                    context_details = gr.Markdown(
                        value="Submit a query to see detailed breakdown"
                    )
            
            # Event handlers
            submit_btn.click(
                fn=self.process_query,
                inputs=[query_input, chatbot, show_viz],
                outputs=[chatbot, query_input, context_viz, context_details]
            )
            
            query_input.submit(
                fn=self.process_query,
                inputs=[query_input, chatbot, show_viz],
                outputs=[chatbot, query_input, context_viz, context_details]
            )
            
            clear_btn.click(
                fn=self.clear_conversation,
                inputs=[],
                outputs=[chatbot, context_viz, context_details]
            )
            
            gr.Markdown("""
            ---
            **Note**: This visualizer uses OpenAI's GPT model and requires an API key in your environment.
            """)
        
        return interface


def launch_ui(
    share: bool = Settings.GRADIO_SHARE,
    server_name: str = Settings.GRADIO_SERVER_NAME,
    server_port: int = Settings.GRADIO_SERVER_PORT
):
    """Launch the Gradio interface"""
    ui = ContextVisualizerUI()
    interface = ui.create_interface()
    interface.launch(
        share=share,
        server_name=server_name,
        server_port=server_port
    )
