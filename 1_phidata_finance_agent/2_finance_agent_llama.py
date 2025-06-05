import os
# Add your GROQ_API_KEY and optionally GROQ_MODEL_ID to a .env file or set them as environment variables.
"""Run `pip install yfinance` to install dependencies."""

from phi.agent import Agent
from phi.model.groq import Groq
from phi.tools.yfinance import YFinanceTools
from dotenv import load_dotenv

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    print("Warning: GROQ_API_KEY not found. Please set it in your .env file or as an environment variable.")


def get_company_symbol(company: str) -> str:
    """Use this function to get the symbol for a company.

    Args:
        company (str): The name of the company.

    Returns:
        str: The symbol for the company.
    """
    # This is a simplified lookup for tutorial purposes.
    # A real application should use a dedicated API or a more comprehensive database for symbol lookups.
    symbols = {
        "Phidata": "MSFT",
        "Infosys": "INFY",
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "Amazon": "AMZN",
        "Google": "GOOGL",
        "Netflix": "NFLX",
        "Nvidia": "NVDA",
    }
    return symbols.get(company, "Unknown")


# YFinanceTools provides the agent with capabilities to fetch stock prices, analyst recommendations, and company fundamentals.
agent = Agent(
    model=Groq(id=os.getenv("GROQ_MODEL_ID", "llama-3.3-70b-versatile")),
    tools=[YFinanceTools(stock_price=True, analyst_recommendations=True, stock_fundamentals=True), get_company_symbol],
    # Instructions guide the agent on how to behave and use its tools.
    instructions=[
        "Use tables to display data.",
        "If you need to find the symbol for a company, use the get_company_symbol tool.",
    ],
    show_tool_calls=True,  # Displays tool calls and their responses.
    markdown=True,  # Outputs responses in Markdown format.
    debug_mode=True,  # Enables detailed logging for debugging.
)

# Example usage of the finance agent
# The agent will use YFinanceTools to get financial data and get_company_symbol to find stock symbols.
# It will then use the Groq model to process this information and generate a response.
try:
    agent.print_response(
        "Summarize and compare analyst recommendations and fundamentals for TSLA and MSFT. Show in tables.", stream=True
    )
except Exception as e:
    print(f"An error occurred: {e}")
