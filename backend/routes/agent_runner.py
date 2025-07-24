from fastapi import APIRouter
from models.request_model import AgentRequest
from services.agent_service import run_agent

router = APIRouter()

@router.post("/run-agent")
def run_agent_endpoint(request: AgentRequest):
    """
    Executes the specified agent with input text and optional model.
    """
    return run_agent(request)
