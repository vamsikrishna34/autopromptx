# utils/output_validator.py

def is_valid_output(output: str) -> bool:
    if not output or len(output.strip()) < 20:
        return False
    if "error" in output.lower() or "failed" in output.lower():
        return False
    return True
