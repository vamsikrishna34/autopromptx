# planner/chain_planner.py

from transformers import pipeline
import logging

class ChainPlanner:
    def __init__(self, model_name="flan-t5-base"):
        self.logger = logging.getLogger(__name__)
        try:
            self.model = pipeline("text2text-generation", model=model_name)
        except Exception as e:
            self.logger.error(f"Failed to load planner model: {e}")
            self.model = None

    def suggest_chain(self, goal: str) -> dict:
        if not self.model:
            return {"error": "Planner model not loaded."}

        prompt = f"Given the goal: '{goal}', suggest a sequence of agents from [SummarizerAgent, CodeReviewerAgent, PersonaAgent, FollowUpAgent, ClarityAgent] to achieve it."
        try:
            result = self.model(prompt)
            raw_output = result[0]["generated_text"]
            return {
                "goal": goal,
                "suggested_chain": raw_output.split(", "),
                "raw_output": raw_output
            }
        except Exception as e:
            self.logger.error(f"Chain suggestion failed: {e}")
            return {"error": str(e)}
