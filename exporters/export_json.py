# exporters/export_json.py

import json

def export_to_json(agent_name: str, model_name: str, output: str, filepath: str):
    data = {
        "agent": agent_name,
        "model": model_name,
        "output": output
    }
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
