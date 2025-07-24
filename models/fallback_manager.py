# models/fallback_manager.py

import json
from config.agent_fallbacks import FALLBACK_CONFIG_PATH
from utils.output_validator import is_valid_output
from utils.dummy_generator import generate_dummy_output

def run_with_fallback(agent, input_text: str) -> str:
    with open(FALLBACK_CONFIG_PATH) as f:
        fallback_map = json.load(f)

    for model_name in fallback_map.get(agent.__class__.__name__, []):
        agent.set_model(model_name)
        output = agent.run(input_text)
        if is_valid_output(output):
            return output

    return generate_dummy_output(agent.__class__.__name__, input_text)
