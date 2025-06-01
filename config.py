"""
Configuration module for AutoPromptX

This module handles API key loading and environment configuration.
"""

import os
from pathlib import Path

# Load OpenAI API key from environment variable
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")

# Default configuration paths
BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = BASE_DIR / "templates"
DATA_DIR = BASE_DIR / "data"
CONFIG_DIR = DATA_DIR / "config"

# Ensure directories exist
os.makedirs(TEMPLATES_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
