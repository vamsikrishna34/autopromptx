import os

# Load OpenAI API key from environment variable or fallback
API_KEY = os.getenv("OPENAI_API_KEY")

if not API_KEY:
    raise EnvironmentError("Please set the OPENAI_API_KEY environment variable.")
