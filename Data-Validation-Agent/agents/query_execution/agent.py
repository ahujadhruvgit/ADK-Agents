from google.adk.agents import Agent
from agents.query_execution.source.agent import source_query_execution_agent
from agents.query_execution.target.agent import target_query_execution_agent

query_execution_agent = Agent(
    name="query_execution_agent",
    description="An agent that can execute queries on source and target databases. It determines whether the query is for the source or target and delegates accordingly.",
    instruction="Your job is to delegate query execution to the correct agent. Look for keywords like 'source' or 'target' in the request to decide which agent to use. If you are unsure, ask for clarification.",
    sub_agents=[source_query_execution_agent, target_query_execution_agent],
)
