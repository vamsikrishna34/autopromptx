# tests/test_utils.py

import pytest
from utils.output_validator import is_valid_output
from utils.dummy_generator import generate_dummy_output

def test_output_validator():
    assert is_valid_output("This is a valid summary.")

def test_dummy_generation():
    dummy = generate_dummy_output("SummarizerAgent", "Some input")
    assert isinstance(dummy, str)
    assert "summary" in dummy.lower()
