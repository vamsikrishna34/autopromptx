# tests/test_agents.py

import pytest
from agents.summarizer_agent import SummarizerAgent

def test_summarizer_output():
    agent = SummarizerAgent()
    output = agent.run("AutoPromptX is a modular GenAI system...")
    assert isinstance(output, str)
    assert len(output) > 20
