from google.adk.agents import LlmAgent
from agents.tools.validation_tool import persist_validation_result

validation_agent = LlmAgent(
    name="validation_agent",
    description="An agent that performs data validation. It takes source and target data as input, compares them, generates a validation summary, and persists the result.",
    instruction="You will be given source data and target data. Your task is to compare them, generate a validation summary, and then use the persist_validation_result tool to save the summary. The summary should have a 'validation_name', a 'status' ('success' or 'failure'), and 'details' of the comparison.",
    model="gemini-2.0-flash",
    tools=[persist_validation_result],
)
