from google.adk.agents import LlmAgent
from tools.search_tool import search_knowledge_base

target_search_agent = LlmAgent(
    name="target_search_agent",
    description="An agent that searches for information in the target knowledge base. It takes a search query as input and returns the results.",
    instruction="You must search the target knowledge base for the given query. Use the search_knowledge_base tool with the scope set to 'target'.",
    model="gemini-2.0-flash",
    tools=[search_knowledge_base],
)
