from agents.base_agent import BaseAgent
from transformers import pipeline
import logging

class SummarizerAgent(BaseAgent):
    def __init__(self, model_name="t5-small"):
        super().__init__(model_name)
        self.logger = logging.getLogger(__name__)
        try:
            self.model = pipeline("summarization", model=self.model_name)
        except Exception as e:
            self.logger.error(f"Model load failed: {e}")
            self.model = None

    def run(self, input_text: str) -> str:
        if not self.model:
            return ""
        try:
            result = self.model(input_text, max_length=100, min_length=30, do_sample=False)
            return result[0]["summary_text"]
        except Exception as e:
            self.logger.error(f"SummarizerAgent failed: {e}")
            return ""
