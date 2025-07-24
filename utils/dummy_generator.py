# utils/dummy_generator.py

def generate_dummy_output(agent_name: str, input_text: str) -> str:
    fallback_messages = {
        "SummarizerAgent": "Summary unavailable. Please review the original text.",
        "CodeReviewerAgent": "No critical issues detected. Consider edge cases.",
        "PersonaAgent": "Could not adjust tone. Original text retained.",
        "FollowUpAgent": "Unable to generate next steps. Please try again.",
        "ClarityAgent": "Clarity score unavailable. Text may need manual review."
    }
    return fallback_messages.get(agent_name, "No output available.")
