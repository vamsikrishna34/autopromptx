from agents.base_agent import BaseAgent
from transformers import pipeline
import logging

class FollowUpAgent(BaseAgent):
    def __init__(self, model_name="flan-t5-base"):
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
        prompt = f"What are the next steps or follow-up actions based on this?\n{input_text}"
        try:
            result = self.model(prompt)
            return result[0]["generated_text"]
        except Exception as e:
            self.logger.error(f"FollowUpAgent failed: {e}")
            return ""
