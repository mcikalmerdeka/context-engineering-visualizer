"""
Context Engineering Visualizer
Main entry point for the application
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

from config import setup_logger
from app.ui import launch_ui

# Setup application logger - this initializes handlers
logger = setup_logger("context_visualizer")

if __name__ == "__main__":
    logger.info("Starting Context Engineering Visualizer")
    launch_ui()
