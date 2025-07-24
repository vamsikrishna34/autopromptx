# models/model_router.py

import json
from config.agent_config import AGENT_CONFIG_PATH
from config.agent_fallbacks import FALLBACK_CONFIG_PATH

def get_model_for_agent(agent_name: str, input_text: str) -> str:
    with open(AGENT_CONFIG_PATH) as f:
        config = json.load(f)
    return config.get(agent_name, "t5-small")
