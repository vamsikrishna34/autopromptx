from agents.base_agent import BaseAgent
from transformers import pipeline
import logging

class PersonaAgent(BaseAgent):
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
        prompt = f"Rewrite this text in a friendly and engaging tone:\n{input_text}"
        try:
            result = self.model(prompt)
            return result[0]["generated_text"]
        except Exception as e:
            self.logger.error(f"PersonaAgent failed: {e}")
            return ""
