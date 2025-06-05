# Build Your First MCP Server: Leave Management
This AI tool helps an HR with leave management related tasks. The codebase here 
is for MCP server that interacts with mock leave database and responds to MCP client queries

# Setup steps
1. Install Claude Desktop
2. Install uv by running `pip install uv`
3. Run `uv init my-first-mcp-server` to create a project directory
4. Run `uv add "mcp[cli]"` to add mcp cli in your project
5. Few folks may get type errors for which you can run `pip install --upgrade typer` to upgrade typer library to its latest version
6. Write code in main.py for leave management server
7. Install this server inside Claude desktop by running `uv run mcp install main.py` in the project directory
8. Kill any running instance of Claude from Task Manager. Restart Claude Desktop
9. In Claude desktop, now you will see tools from this server

# Database Information
- This server uses an SQLite database named `leave_management.db`.
- When you run the server (e.g., using `python main.py` or via the MCP client interaction if it's started by the client environment), this database file will be automatically created in the `2_mcp_leave_management/` directory if it doesn't already exist.
- The database is also automatically initialized with sample employee data and leave history upon its first creation, allowing you to test the tools immediately.

@All rights reserved. Codebasics Inc. LearnerX Pvt Ltd. 
