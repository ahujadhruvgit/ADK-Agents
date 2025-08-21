from google.adk.agents import LlmAgent, tool
from tools.database_tools import execute_sql_query_source, execute_sql_query_target
from config.settings import SUB_AGENT_MODEL, SOURCE_DB_CONNECTION_NAME, TARGET_DB_CONNECTION_NAME

class SourceSearchAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="SourceSearchAgent",
            description="Discovers metadata and schema information from the source data system.",
            instruction="""You are a specialized agent for discovering metadata and schema details
                           from the source database. Use the 'execute_sql_query_source' tool to query
                           information schema views (e.g., INFORMATION_SCHEMA.COLUMNS, INFORMATION_SCHEMA.TABLES)
                           to retrieve table names, column names, data types, and other relevant metadata.
                           Return the discovered schema information in a structured format.""",
            tools=[execute_sql_query_source]
        )

    @tool
    async def discover_schema(self, table_name: str) -> dict:
        """
        Discovers schema information for a given table in the source database.
        This is a simplified example; real-world schema discovery can be more complex.
        The query assumes a database with INFORMATION_SCHEMA like MySQL or PostgreSQL.
        Adjust query based on specific database type (BigQuery, Spanner, etc.) if needed.

        Args:
            table_name (str): The full name of the table (e.g., 'my_dataset.my_table').
        Returns:
            dict: A dictionary containing schema details.
        """
        print(f"Source Search Agent: Discovering schema for table: {table_name}")
        # Extract table name without schema/dataset for INFORMATION_SCHEMA query
        simple_table_name = table_name.split('.')[-1]
        schema_query = f"""
        SELECT column_name, data_type, is_nullable
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_name = '{simple_table_name}'
        ORDER BY ordinal_position;
        """
        try:
            results = await self.tools.execute_sql_query_source(query=schema_query, database_name=SOURCE_DB_CONNECTION_NAME)
            if results and results.get("rows"):
                columns = results.get("columns",)
                schema_details = []
                for row in results["rows"]:
                    col_info = {columns[i]: row[i] for i in range(len(columns))}
                    schema_details.append(col_info)
                print(f"Source Search Agent: Discovered schema: {schema_details}")
                return {"status": "success", "table": table_name, "schema": schema_details}
            else:
                return {"status": "success", "table": table_name, "schema":schema_details, "message": "No schema found or table does not exist."} # Corrected syntax
        except Exception as e:
            print(f"Source Search Agent: Error discovering schema: {e}")
            return {"status": "failed", "error": str(e)}

class TargetSearchAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="TargetSearchAgent",
            description="Discovers metadata and schema information from the target data system.",
            instruction="""You are a specialized agent for discovering metadata and schema details
                           from the target database. Use the 'execute_sql_query_target' tool to query
                           information schema views (e.g., INFORMATION_SCHEMA.COLUMNS, INFORMATION_SCHEMA.TABLES)
                           to retrieve table names, column names, data types, and other relevant metadata.
                           Return the discovered schema information in a structured format.""",
            tools=[execute_sql_query_target]
        )

    @tool
    async def discover_schema(self, table_name: str) -> dict:
        """
        Discovers schema information for a given table in the target database.
        This is a simplified example; real-world schema discovery can be more complex.
        The query assumes a database with INFORMATION_SCHEMA like MySQL or PostgreSQL.
        Adjust query based on specific database type (BigQuery, Spanner, etc.) if needed.

        Args:
            table_name (str): The full name of the table (e.g., 'my_dataset.my_table').
        Returns:
            dict: A dictionary containing schema details.
        """
        print(f"Target Search Agent: Discovering schema for table: {table_name}")
        # Extract table name without schema/dataset for INFORMATION_SCHEMA query
        simple_table_name = table_name.split('.')[-1]
        schema_query = f"""
        SELECT column_name, data_type, is_nullable
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_name = '{simple_table_name}'
        ORDER BY ordinal_position;
        """
        try:
            results = await self.tools.execute_sql_query_target(query=schema_query, database_name=TARGET_DB_CONNECTION_NAME)
            if results and results.get("rows"):
                columns = results.get("columns",)
                schema_details = []
                for row in results["rows"]:
                    col_info = {columns[i]: row[i] for i in range(len(columns))}
                    schema_details.append(col_info)
                print(f"Target Search Agent: Discovered schema: {schema_details}")
                return {"status": "success", "table": table_name, "schema": schema_details}
            else:
                return {"status": "success", "table": table_name, "schema": schema_details, "message": "No schema found or table does not exist."} # Corrected syntax
        except Exception as e:
            print(f"Target Search Agent: Error discovering schema: {e}")
            return {"status": "failed", "error": str(e)}