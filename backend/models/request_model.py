from pydantic import BaseModel

class AgentRequest(BaseModel):
    agent_name: str
    input_text: str
    model_name: str | None = None  # Optional field
