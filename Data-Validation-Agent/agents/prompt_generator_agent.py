from google.adk.agents import LlmAgent
from config.settings import SUB_AGENT_MODEL, FIRESTORE_PROMPT_TEMPLATES_COLLECTION
from tools.prompt_generation_tools import retrieve_prompt_template, retrieve_context_for_prompt

class PromptGeneratorAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="PromptGeneratorAgent",
            description="Dynamically generates and refines prompts for other agents.",
            instruction="""You are a specialized agent for crafting precise and effective prompts
                           for other AI agents. Your goal is to ensure that prompts are clear,
                           contextually rich, and include all necessary objectives, constraints,
                           and output specifications to guide the target agent's reasoning and tool usage.
                           You can retrieve prompt templates and contextual information to enhance prompts.""",
            tools=[retrieve_prompt_template, retrieve_context_for_prompt] # Tools added here
        )

    async def generate_validation_plan_prompt(self, validation_request: dict, template_name: str = "default_validation_plan") -> str:
        """
        Generates a detailed prompt for the Root Agent or Validation Agent to plan a validation.

        Args:
            validation_request (dict): The initial high-level validation request.
            template_name (str): The name of the prompt template to retrieve.
        Returns:
            str: A refined prompt string.
        """
        print(f"Prompt Generator Agent: Generating prompt for validation request: {validation_request}")

        # Retrieve a prompt template
        template_data = await self.tools.retrieve_prompt_template(template_name, FIRESTORE_PROMPT_TEMPLATES_COLLECTION)
        base_template = template_data.get("template_content", "No template found. Defaulting to basic prompt.")

        # Retrieve additional context (conceptual)
        # context_info = await self.tools.retrieve_context_for_prompt(validation_request.get("source_table"))

        source_table = validation_request.get("source_table", "N/A")
        target_table = validation_request.get("target_table", "N/A")
        validation_rules = validation_request.get("validation_rules",)

        rules_description = ""
        if validation_rules:
            rules_description = "\n".join()
        else:
            rules_description = "No specific rules provided. Perform a default comprehensive validation."

        # Combine template, request details, and context
        prompt = base_template.format(
            source_table=source_table,
            target_table=target_table,
            rules_description=rules_description
            # Add other context variables here
        )

        print("Prompt Generator Agent: Prompt generated.")
        return prompt