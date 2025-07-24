from agents.summarizer_agent import SummarizerAgent
from agents.code_reviewer_agent import CodeReviewerAgent
from agents.persona_agent import PersonaAgent
from agents.followup_agent import FollowUpAgent
from agents.clarity_agent import ClarityAgent

def run_agent(request):
    agent = request.agent_name
    input_text = request.input_text
    model = request.model_name or "auto"

    try:
        # Dynamically select agent class
        if agent == "SummarizerAgent":
            agent_instance = SummarizerAgent(model_name=model)
        elif agent == "CodeReviewerAgent":
            agent_instance = CodeReviewerAgent(model_name=model)
        elif agent == "PersonaAgent":
            agent_instance = PersonaAgent(model_name=model)
        elif agent == "FollowUpAgent":
            agent_instance = FollowUpAgent(model_name=model)
        elif agent == "ClarityAgent":
            agent_instance = ClarityAgent(model_name=model)
        else:
            return {"error": f"Unknown agent: {agent}"}

        # Run the agent
        output = agent_instance.run(input_text)
        return {"output": output}

    except Exception as e:
        return {"error": f"Agent execution failed: {str(e)}"}
