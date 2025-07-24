from agents.base_agent import BaseAgent
from transformers import pipeline
import logging

class CodeReviewerAgent(BaseAgent):
    def __init__(self, model_name="Salesforce/codet5-small"):
        super().__init__(model_name)
        self.logger = logging.getLogger(__name__)
        try:
            self.model = pipeline("text2text-generation", model=self.model_name)
        except Exception as e:
            self.logger.error(f"Model load failed: {e}")
            self.model = None

    def run(self, input_text: str) -> str:
        if not self.model:
            return ""
        prompt = f"Review this code and suggest improvements:\n{input_text}"
        try:
            result = self.model(prompt)
            return result[0]["generated_text"]
        except Exception as e:
            self.logger.error(f"CodeReviewerAgent failed: {e}")
            return ""
