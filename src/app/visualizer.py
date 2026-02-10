"""Context window visualization component"""

from typing import Dict, Any
from datetime import datetime


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
        
    def get_summary(self) -> Dict[str, Any]:
        """Get structured summary of context"""
        return {
            "layers": [l["layer"] for l in self.context_layers],
            "total_tokens": sum(self.token_counts.values()),
            "breakdown": self.token_counts
        }
