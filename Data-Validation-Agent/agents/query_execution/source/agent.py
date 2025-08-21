from google.adk.agents import LlmAgent
from tools.query_execution_tool import execute_query

source_query_execution_agent = LlmAgent(
    name="source_query_execution_agent",
    description="An agent that executes queries on the source database. It takes a query as input and returns the result.",
    instruction="You must execute the given query on the source database. Use the execute_query tool with the connection_id set to 'source_db'.",
    model="gemini-2.0-flash",
    tools=[execute_query],
)
