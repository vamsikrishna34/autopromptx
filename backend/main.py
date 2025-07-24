from fastapi import FastAPI
from routes.agent_runner import router as agent_router

app = FastAPI(
    title="AutoPromptX Backend",
    description="Modular GenAI agent orchestration API",
    version="1.0.0"
)

# Include agent execution routes
app.include_router(agent_router, prefix="/api")
