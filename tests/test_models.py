# tests/test_models.py

import pytest
from models.model_router import get_model_for_agent

def test_model_router_default():
    model = get_model_for_agent("SummarizerAgent", "Some input")
    assert model in ["t5-small", "flan-t5-base"]
