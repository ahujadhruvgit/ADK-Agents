from google.adk.agents import Agent
from agents.search.source.agent import source_search_agent
from agents.search.target.agent import target_search_agent

search_agent = Agent(
    name="search_agent",
    description="An agent that can search for information in the source and target knowledge bases. It determines whether the search is for the source or target and delegates accordingly.",
    instruction="Your job is to delegate the search to the correct agent. Look for keywords like 'source' or 'target' in the request to decide which agent to use. If you are unsure, ask for clarification.",
    sub_agents=[source_search_agent, target_search_agent],
)
