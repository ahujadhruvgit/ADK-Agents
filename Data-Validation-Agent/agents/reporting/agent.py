from google.adk.agents import LlmAgent

reporting_agent = LlmAgent(
    name="reporting_agent",
    description="An agent that generates human-readable reports from validation results.",
    instruction="You will be given one or more validation results. Your task is to generate a clear and concise summary report. The report should highlight any failures and provide a high-level overview of the validation outcomes.",
    model="gemini-2.0-flash",
)
