import os
# Add your GROQ_API_KEY and optionally GROQ_MODEL_ID to a .env file or set them as environment variables.
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    print("Warning: GROQ_API_KEY not found. Please set it in your .env file or as an environment variable.")


# Create a simple agent with a Groq model
agent = Agent(
    model=Groq(id=os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile"))
    # No specific instructions or tools are provided, so it will use the model's default capabilities.
)

# Example usage of the agent
try:
    agent.print_response("Share a 2 sentence love story between dosa and samosa")
except Exception as e:
    print(f"An error occurred: {e}")