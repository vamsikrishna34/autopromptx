# cli/run_chain.py

import logging
from cli.cli_utils import parse_arguments
from agents.summarizer_agent import SummarizerAgent
from agents.code_revieweragent import CodeReviewerAgent
from agents.persona_agent import PersonaAgent
from agents.followup_agent import FollowUpAgent
from agents.clarity_agent import ClarityAgent
from models.model_router import get_model_for_agent
from models.fallback_manager import run_with_fallback

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGENT_MAP = {
    "SummarizerAgent": SummarizerAgent,
    "CodeReviewerAgent": CodeReviewerAgent,
    "PersonaAgent": PersonaAgent,
    "FollowUpAgent": FollowUpAgent,
    "ClarityAgent": ClarityAgent
}

def main():
    args = parse_arguments()
    agent_class = AGENT_MAP.get(args.agent)

    if not agent_class:
        logger.error(f"Unknown agent: {args.agent}")
        return

    agent = agent_class()

    # Model selection
    if args.mode == "manual" and args.model:
        agent.set_model(args.model)
    else:
        selected_model = get_model_for_agent(args.agent, args.input)
        agent.set_model(selected_model)

    # Run with fallback logic
    output = run_with_fallback(agent, args.input)

    # Display structured output
    print("\n=== AutoPromptX Output ===")
    print(f"Agent: {args.agent}")
    print(f"Model: {agent.model_name}")
    print(f"Output:\n{output}")

if __name__ == "__main__":
    main()
