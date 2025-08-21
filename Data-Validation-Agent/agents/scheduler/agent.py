from google.adk.agents import LlmAgent

scheduler_agent = LlmAgent(
    name="scheduler_agent",
    description="An agent that initiates a data validation process based on a schedule. This agent is the entrypoint for tasks triggered by the external Cloud Scheduler.",
    instruction="You have been triggered by an external scheduler to start a data validation run. You will be given a prompt that was stored in the database. Your task is to take this prompt and begin the data validation workflow by coordinating with the other agents.",
    model="gemini-2.0-flash",
)
