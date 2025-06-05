import os
# Add your OPENAI_API_KEY (and optionally OPENAI_MODEL_ID) and/or GROQ_API_KEY (and optionally GROQ_MODEL_ID)
# to a .env file or set them as environment variables, depending on the model used.
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.model.groq import Groq
from phi.tools.duckduckgo import DuckDuckGo
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()
# Default model is OpenAI, so check for OPENAI_API_KEY first.
if not os.getenv("OPENAI_API_KEY"):
    print("Warning: OPENAI_API_KEY not found. Please set it in your .env file or as an environment variable if you plan to use OpenAI models.")
if not os.getenv("GROQ_API_KEY"):
    print("Warning: GROQ_API_KEY not found. Please set it in your .env file or as an environment variable if you plan to use Groq models.")

# --- Choosing between OpenAI and Groq Models ---
# This script defaults to using OpenAI models (gpt-4o specified by OPENAI_MODEL_ID).
# To use Groq models (e.g., llama-3.3-70b-versatile specified by GROQ_MODEL_ID):
# 1. Comment out the `model=OpenAIChat(...)` line for each agent definition below.
# 2. Uncomment the `model=Groq(...)` line for each agent definition.
#
# Ensure the relevant API keys (OPENAI_API_KEY, GROQ_API_KEY) and any chosen
# model IDs (OPENAI_MODEL_ID, GROQ_MODEL_ID) are set in your environment,
# typically in a .env file at the root of your project.

# Web Agent: Specialist agent with web search capabilities using DuckDuckGo.
web_agent = Agent(
    name="Web Agent",
    # model=Groq(id=os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")),
    model=OpenAIChat(id=os.getenv("OPENAI_MODEL_ID", "gpt-4o")),
    tools=[DuckDuckGo()],
    instructions=["Always include sources"],
    show_tool_calls=True,  # Displays tool calls and their responses.
    markdown=True  # Outputs responses in Markdown format.
)

# Finance Agent: Specialist agent with financial data fetching capabilities using YFinanceTools.
finance_agent = Agent(
    name="Finance Agent",
    role="Get financial data",
    # model=Groq(id=os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")),
    model=OpenAIChat(id=os.getenv("OPENAI_MODEL_ID", "gpt-4o")),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, company_info=True)],
    instructions=["Use tables to display data"],
    show_tool_calls=True,  # Displays tool calls and their responses.
    markdown=True,  # Outputs responses in Markdown format.
)

# Agent Team: Supervisor agent that delegates tasks to specialist agents (Web Agent, Finance Agent)
# based on the nature of the prompt. It coordinates the work of the team.
agent_team = Agent(
    # model=Groq(id=os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")),
    model=OpenAIChat(id=os.getenv("OPENAI_MODEL_ID", "gpt-4o")),
    team=[web_agent, finance_agent],
    instructions=["Always include sources", "Use tables to display data"],
    show_tool_calls=True,  # Displays tool calls and their responses for the team.
    markdown=True,  # Outputs the final response in Markdown format.
)

# Example usage of the agent team
# The team will delegate tasks to the Web Agent for news and Finance Agent for financial data.
try:
    agent_team.print_response("Summarize analyst recommendations and share the latest news for NVDA", stream=True)
except Exception as e:
    print(f"An error occurred: {e}")
