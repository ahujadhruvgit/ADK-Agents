from google.adk.agents import LlmAgent
from tools.database_tools import execute_sql_query_source, execute_sql_query_target
from config.settings import SUB_AGENT_MODEL

class SourceQueryExecutionAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="SourceQueryExecutionAgent",
            description="Executes SQL queries against the source data system via MCP Toolbox.",
            instruction="""You are a specialized agent for executing queries on the source database.
                           You must use the 'execute_sql_query_source' tool to run SQL queries.
                           Ensure queries are safe and efficient. Return the query results.""",
            tools=[execute_sql_query_source]
        )

    async def execute_query(self, query_text: str, database_name: str) -> dict:
        """
        Executes a given SQL query against the source database.
        Args:
            query_text (str): The SQL query to execute.
            database_name (str): The logical name of the source database connection (as configured in MCP Toolbox).
        Returns:
            dict: The query results, including status and data.
        """
        print(f"Source Query Execution Agent: Executing query on source '{database_name}': {query_text}")
        try:
            results = await self.tools.execute_sql_query_source(query=query_text, database_name=database_name)
            print(f"Source Query Execution Agent: Query results: {results}")
            return {"status": "success", "data": results}
        except Exception as e:
            print(f"Source Query Execution Agent: Error executing query: {e}")
            return {"status": "failed", "error": str(e)}

class TargetQueryExecutionAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="TargetQueryExecutionAgent",
            description="Executes SQL queries against the target data system via MCP Toolbox.",
            instruction="""You are a specialized agent for executing queries on the target database.
                           You must use the 'execute_sql_query_target' tool to run SQL queries.
                           Ensure queries are safe and efficient. Return the query results.""",
            tools=[execute_sql_query_target]
        )

    async def execute_query(self, query_text: str, database_name: str) -> dict:
        """
        Executes a given SQL query against the target database.
        Args:
            query_text (str): The SQL query to execute.
            database_name (str): The logical name of the target database connection (as configured in MCP Toolbox).
        Returns:
            dict: The query results, including status and data.
        """
        print(f"Target Query Execution Agent: Executing query on target '{database_name}': {query_text}")
        try:
            results = await self.tools.execute_sql_query_target(query=query_text, database_name=database_name)
            print(f"Target Query Execution Agent: Query results: {results}")
            return {"status": "success", "data": results}
        except Exception as e:
            print(f"Target Query Execution Agent: Error executing query: {e}")
            return {"status": "failed", "error": str(e)}