# utils/token_counter.py

from transformers import AutoTokenizer

def count_tokens(text: str, model_name: str = "t5-small") -> int:
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    tokens = tokenizer.encode(text, truncation=True)
    return len(tokens)
