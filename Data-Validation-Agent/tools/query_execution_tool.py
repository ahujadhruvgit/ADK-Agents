def execute_query(query: str, connection_id: str) -> dict:
    """
    Executes a query against a specified database.

    Args:
        query: The SQL query to execute.
        connection_id: The identifier for the database connection (e.g., 'source_db', 'target_db').

    Returns:
        A dictionary with the query result.
    """
    print(f"--- Tool: Executing query '{query}' on '{connection_id}' ---")
    # In a real implementation, this tool would connect to the database
    # and execute the query. For now, we'll return mock data.
    if "source" in connection_id:
        return {"status": "success", "data": [{"id": 1, "name": "test_source"}]}
    elif "target" in connection_id:
        return {"status": "success", "data": [{"id": 1, "name": "test_target"}]}
    else:
        return {"status": "error", "message": f"Unknown connection_id: {connection_id}"}
