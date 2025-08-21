from google.adk.agents import Agent
from agents.search.agent import search_agent
from agents.query_execution.agent import query_execution_agent
from agents.validation.agent import validation_agent
from agents.reporting.agent import reporting_agent
from agents.prompt_generator.agent import prompt_generator_agent
from agents.scheduler.agent import scheduler_agent

# Note: For these imports to work, the root of the project ('Data-Validation-Agent')
# must be in the Python path. This is a standard setup for ADK projects.
# The __init__.py files in each directory help Python recognize them as packages.

root_agent = Agent(
    name="data_validation_root_agent",
    description="The root agent for the data validation system. It orchestrates the other agents to perform data validation tasks based on user requests or scheduled triggers.",
    instruction="""You are the orchestrator of a multi-agent data validation system.
Your primary role is to understand incoming requests and delegate tasks to the appropriate sub-agent.

- For requests to **run a validation**, you will need to coordinate a workflow:
  1. Use the `query_execution_agent` to get data from source and target.
  2. Pass the data to the `validation_agent` to perform the comparison.
  3. Use the `reporting_agent` to generate a summary of the results.
- For requests to **find information** about past validations or other topics, use the `search_agent`.
- For requests to **create a new validation task**, use the `prompt_generator_agent`.
- For tasks initiated by the **scheduler**, the `scheduler_agent` is the entry point. You will then take over the orchestration.

Carefully examine the user's intent to choose the correct sub-agent or sequence of agents.
""",
    sub_agents=[
        search_agent,
        query_execution_agent,
        validation_agent,
        reporting_agent,
        prompt_generator_agent,
        scheduler_agent,
    ],
)