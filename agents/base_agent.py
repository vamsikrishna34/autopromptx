from abc import ABC, abstractmethod
from typing import Optional

class BaseAgent(ABC):
    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name
        self.model = None

    @abstractmethod
    def run(self, input_text: str) -> str:
        pass

    def set_model(self, model_name: str):
        self.model_name = model_name
