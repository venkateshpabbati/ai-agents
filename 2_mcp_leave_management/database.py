"""
Handles SQLite database operations for the Leave Management System.

This module includes functions for:
- Establishing database connections.
- Creating necessary tables (`employees`, `leave_history`) if they don't exist.
- Initializing the database with sample employee data and leave history.
- Retrieving employee leave balance and history.
- Updating employee leave balances and adding new leave entries.

The database file is named `leave_management.db` and is located in the
`2_mcp_leave_management` directory.
"""
import sqlite3
from typing import List, Dict, Any, Tuple


DATABASE_NAME = "2_mcp_leave_management/leave_management.db"


def get_db_connection() -> sqlite3.Connection:
    """Establishes a connection to the SQLite database."""
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row  # Access columns by name
    return conn

def create_tables_if_not_exist():
    """Creates the necessary tables if they don't already exist."""
    # Ensures that the employees and leave_history tables are created before any operations.
    conn = get_db_connection()
    cursor = conn.cursor()

    # Employee table: stores employee ID and their current leave balance
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employees (
        employee_id TEXT PRIMARY KEY,
        balance INTEGER NOT NULL
    )
    ''')

    # Leave history table: stores individual leave dates for each employee
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS leave_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id TEXT NOT NULL,
        leave_date TEXT NOT NULL,
        FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
    )
    ''')
    conn.commit()
    conn.close()

def initialize_database_with_sample_data():
    """Populates the database with initial sample data if it's empty."""
    # Idempotent function: only adds data if the 'employees' table is currently empty.
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if employees table is empty
    cursor.execute("SELECT COUNT(*) FROM employees")
    if cursor.fetchone()[0] == 0:
        sample_employees: List[Tuple[str, int]] = [
            ("E001", 18),
            ("E002", 20)
        ]
        cursor.executemany("INSERT INTO employees (employee_id, balance) VALUES (?, ?)", sample_employees)

        sample_leave_history: List[Tuple[str, str]] = [
            ("E001", "2024-12-25"),
            ("E001", "2025-01-01")
        ]
        cursor.executemany("INSERT INTO leave_history (employee_id, leave_date) VALUES (?, ?)", sample_leave_history)

        conn.commit()
    conn.close()

def get_employee_data(employee_id: str) -> Dict[str, Any]:
    """Retrieves employee balance and history. Returns None if employee_id is not found."""
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT balance FROM employees WHERE employee_id = ?", (employee_id,))
    employee_row = cursor.fetchone()

    if not employee_row:
        conn.close()
        return None

    balance = employee_row["balance"]

    cursor.execute("SELECT leave_date FROM leave_history WHERE employee_id = ? ORDER BY leave_date", (employee_id,))
    history_rows = cursor.fetchall()
    history = [row["leave_date"] for row in history_rows]

    conn.close()
    return {"balance": balance, "history": history}

def update_employee_leave(employee_id: str, new_balance: int, leave_dates_to_add: List[str]) -> bool:
    """
    Updates an employee's leave balance and adds new leave dates to their history.
    This operation is transactional: either all changes are committed or none are.
    Returns True if successful, False otherwise.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Update employee's balance
        cursor.execute("UPDATE employees SET balance = ? WHERE employee_id = ?", (new_balance, employee_id))
        if cursor.rowcount == 0:  # No rows updated means employee_id was not found
            conn.close()
            return False  # Employee not found, or no update was needed (though balance change implies it was)

        # Add new leave dates to history
        if leave_dates_to_add:
            history_data: List[Tuple[str, str]] = [(employee_id, date_str) for date_str in leave_dates_to_add]
            cursor.executemany("INSERT INTO leave_history (employee_id, leave_date) VALUES (?, ?)", history_data)

        conn.commit()  # Commit transaction
        return True
    except sqlite3.Error as e:  # Catch any SQLite-related errors
        conn.rollback()  # Rollback transaction in case of any error during DB operations
        # Optionally, log the error e here
        return False
    finally:
        conn.close()

# Initialize tables and data when this module is loaded
create_tables_if_not_exist()
initialize_database_with_sample_data()

if __name__ == '__main__':
    # Example usage for testing the database module directly
    print("Database module initialized.")
    print("Data for E001:", get_employee_data("E001"))
    print("Data for E002:", get_employee_data("E002"))
    print("Data for E003 (non-existent):", get_employee_data("E003"))

    # Example apply leave
    # print("\nAttempting to apply leave for E002...")
    # if get_employee_data("E002")['balance'] >= 2:
    #     new_dates = ["2025-03-10", "2025-03-11"]
    #     current_balance = get_employee_data("E002")['balance']
    #     if update_employee_leave("E002", current_balance - len(new_dates), new_dates):
    #         print("Leave applied successfully for E002.")
    #         print("Updated data for E002:", get_employee_data("E002"))
    #     else:
    #         print("Failed to apply leave for E002.")
    # else:
    #     print("E002 has insufficient balance for this example.")
