import requests
from google.adk.agents import tool
from config.settings import MCP_TOOLBOX_BASE_URL, MCP_TOOLBOX_API_KEY

@tool
async def execute_sql_query_source(query: str, database_name: str) -> dict:
    """
    Executes a SQL query against the source database via the MCP Toolbox.
    The MCP Toolbox handles the actual database connection and query execution.

    Args:
        query (str): The SQL query to execute.
        database_name (str): The logical name of the database connection
                             (as configured in the MCP Toolbox).
    Returns:
        dict: A dictionary containing the query results.
              Example: {"columns": ["col1", "col2"], "rows": [[val1, val2],...]}
    Raises:
        requests.exceptions.RequestException: If the API call to MCP Toolbox fails.
    """
    print(f"Tool: Sending query to MCP Toolbox for source '{database_name}': {query}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MCP_TOOLBOX_API_KEY}" # Or other authentication method
    }
    payload = {
        "database_name": database_name,
        "query": query,
        # Add other parameters as required by your MCP Toolbox setup, e.g., schema, table
    }
    try:
        response = requests.post(f"{MCP_TOOLBOX_BASE_URL}/query", json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()
        print(f"Tool: Received response from MCP Toolbox: {result}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Tool: Error communicating with MCP Toolbox: {e}")
        raise

@tool
async def execute_sql_query_target(query: str, database_name: str) -> dict:
    """
    Executes a SQL query against the target database via the MCP Toolbox.
    The MCP Toolbox handles the actual database connection and query execution.

    Args:
        query (str): The SQL query to execute.
        database_name (str): The logical name of the database connection
                             (as configured in the MCP Toolbox).
    Returns:
        dict: A dictionary containing the query results.
              Example: {"columns": ["col1", "col2"], "rows": [[val1, val2],...]}
    Raises:
        requests.exceptions.RequestException: If the API call to MCP Toolbox fails.
    """
    print(f"Tool: Sending query to MCP Toolbox for target '{database_name}': {query}")
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {MCP_TOOLBOX_API_KEY}" # Or other authentication method
    }
    payload = {
        "database_name": database_name,
        "query": query,
        # Add other parameters as required by your MCP Toolbox setup, e.g., schema, table
    }
    try:
        response = requests.post(f"{MCP_TOOLBOX_BASE_URL}/query", json=payload, headers=headers)
        response.raise_for_status() # Raise an exception for HTTP errors (4xx or 5xx)
        result = response.json()
        print(f"Tool: Received response from MCP Toolbox: {result}")
        return result
    except requests.exceptions.RequestException as e:
        print(f"Tool: Error communicating with MCP Toolbox: {e}")
        raise