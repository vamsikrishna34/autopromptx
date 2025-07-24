# Example fallback logic for AutoPromptX

fallback_map = {
    "SummarizerAgent": ["t5-small", "flan-t5-base", "google/pegasus-xsum"],
    "CodeReviewerAgent": ["Salesforce/codet5-small", "t5-base"],
    "PersonaAgent": ["flan-t5-base", "t5-v1_1-base"],
    "FollowUpAgent": ["flan-t5-base", "t5-small"],
    "ClarityAgent": ["flan-t5-base", "t5-small"]
}

def get_fallback_models(agent_name):
    return fallback_map.get(agent_name, [])
