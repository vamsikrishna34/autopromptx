# cli/cli_utils.py

import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run AutoPromptX agent from CLI")
    parser.add_argument("--agent", type=str, required=True, help="Agent name (e.g., SummarizerAgent)")
    parser.add_argument("--input", type=str, required=True, help="Input text to process")
    parser.add_argument("--model", type=str, default=None, help="Optional: manually specify model")
    parser.add_argument("--mode", type=str, choices=["auto", "manual"], default="auto", help="Model selection mode")
    return parser.parse_args()
