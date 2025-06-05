"""
Main MCP server file for the Leave Management Tutorial.

This script defines an MCP (My Computational Platform) server with tools for:
- Checking employee leave balances.
- Applying for leave, with validation for dates and availability.
- Retrieving employee leave history.

It integrates with `database.py` to persist leave data in an SQLite database.
The server is an instance of FastMCP, named "LeaveManager".
"""
from mcp.server.fastmcp import FastMCP
from typing import List
from . import database # Use relative import for modules within the same package
import datetime
import re


# Create MCP server instance, naming it "LeaveManager"
mcp = FastMCP("LeaveManager")


# --- Tool Definitions ---

@mcp.tool()
def get_leave_balance(employee_id: str) -> str:
    """
    Checks the remaining leave balance for a given employee ID.
    Example: "How many leave days does E001 have?"
    """
    data = database.get_employee_data(employee_id)
    if data:
        return f"Employee {employee_id} has {data['balance']} leave days remaining."
    return "Employee ID not found."

# Tool: Apply for Leave with specific dates
@mcp.tool()
def apply_leave(employee_id: str, leave_dates: List[str]) -> str:
    """
    Apply leave for an employee for one or more specific dates.
    Dates should be provided in "YYYY-MM-DD" format (e.g., ["2025-04-17", "2025-05-01"]).
    The tool validates date formats, checks if dates are in the past,
    verifies if dates are already booked, and ensures sufficient leave balance.
    Example: "Apply leave for E001 on 2025-06-10 and 2025-06-11"
    """
    # Fetch employee data from the database
    data = database.get_employee_data(employee_id)
    if not data:
        return "Employee ID not found."

    if not leave_dates:
        return "No leave dates provided. Please specify the dates you want to apply for."

    parsed_leave_dates = []
    today = datetime.date.today()
    current_history = data.get('history', [])  # Default to empty list if no history

    # Validate each date provided
    for date_str in leave_dates:
        # Check format "YYYY-MM-DD"
        if not re.match(r"^\d{4}-\d{2}-\d{2}$", date_str):
            return f"Invalid date format: '{date_str}'. Please use YYYY-MM-DD format."
        # Check if the date is valid (e.g., not 2023-02-30)
        try:
            leave_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return f"Invalid date value: '{date_str}'. Please ensure dates are correct (e.g., not 2023-02-30)."

        # Check if the date is in the past
        if leave_date < today:
            return f"Cannot apply for leave in the past: '{date_str}' is before today ({today})."

        # Check if the date is already booked
        if date_str in current_history:
            return f"Date {date_str} is already booked as leave for employee {employee_id}."

        parsed_leave_dates.append(date_str)  # Store validated dates (original string format)

    # Check for sufficient balance
    requested_days = len(parsed_leave_dates)
    available_balance = data["balance"]

    if available_balance < requested_days:
        return f"Insufficient leave balance for {employee_id}. Requested: {requested_days} day(s), Available: {available_balance}."

    # Update database
    new_balance = available_balance - requested_days
    if database.update_employee_leave(employee_id, new_balance, parsed_leave_dates):
        return f"Leave applied successfully for {requested_days} day(s) for {employee_id}. New balance: {new_balance}."
    else:
        # This case might indicate a concurrent modification or unexpected DB issue.
        return "Failed to update leave records in the database. Please try again or contact support if the issue persists."


@mcp.tool()
def get_leave_history(employee_id: str) -> str:
    """
    Retrieves the leave history for a given employee ID.
    Returns a list of dates or a message if no leave has been taken.
    Example: "Show me the leave history for E002"
    """
    data = database.get_employee_data(employee_id)
    if data:
        history_list = data['history']
        if history_list:
            # Format for better readability if there are many dates
            history_str = ', '.join(sorted(list(set(history_list)))) # Sort and remove duplicates for display
            return f"Leave history for employee {employee_id}: {history_str}."
        else:
            return f"Employee {employee_id} has no leave history."
    return "Employee ID not found."


# --- Resource Definitions ---

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """
    Provides a personalized greeting.
    This is a simple resource example.
    Example URI: greeting://Alice
    """
    return f"Hello, {name}! How can I assist you with leave management today?"


# --- Server Execution ---

if __name__ == "__main__":
    # This allows running the MCP server directly using `python main.py`
    # The database (leave_management.db) will be created/updated in the same directory.
    mcp.run()
