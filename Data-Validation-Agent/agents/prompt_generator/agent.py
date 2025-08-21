from google.adk.agents import LlmAgent
from tools.prompt_generator_tool import call_prompt_generator

prompt_generator_agent = LlmAgent(
    name="prompt_generator_agent",
    description="An agent that generates prompts for data validation tasks based on high-level requests.",
    instruction="Your task is to convert a high-level data validation request (e.g., 'validate table X between source and target') into a detailed, specific prompt that the root validation agent can execute. Once the prompt is generated, you must use the call_prompt_generator tool to store it.",
    model="gemini-2.0-flash",
    tools=[call_prompt_generator],
)
