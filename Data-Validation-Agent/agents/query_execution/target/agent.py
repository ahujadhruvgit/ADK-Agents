from google.adk.agents import LlmAgent
from tools.query_execution_tool import execute_query

target_query_execution_agent = LlmAgent(
    name="target_query_execution_agent",
    description="An agent that executes queries on the target database. It takes a query as input and returns the result.",
    instruction="You must execute the given query on the target database. Use the execute_query tool with the connection_id set to 'target_db'.",
    model="gemini-2.0-flash",
    tools=[execute_query],
)
