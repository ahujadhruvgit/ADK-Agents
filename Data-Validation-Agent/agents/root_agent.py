from google.adk.agents import LlmAgent, WorkflowAgent
from agents.search_agent import SourceSearchAgent, TargetSearchAgent
from agents.query_execution_agent import SourceQueryExecutionAgent, TargetQueryExecutionAgent
from agents.validation_agent import ValidationAgent
from agents.reporting_agent import ReportingAgent
from agents.prompt_generator_agent import PromptGeneratorAgent
from agents.scheduler_agent import SchedulerAgent
from config.settings import ROOT_AGENT_MODEL, SUB_AGENT_MODEL, SOURCE_DB_CONNECTION_NAME, TARGET_DB_CONNECTION_NAME

class DataValidationRootAgent(LlmAgent):
    def __init__(self, model_name: str = ROOT_AGENT_MODEL):
        # Initialize sub-agents
        self.source_search_agent = SourceSearchAgent(model_name=SUB_AGENT_MODEL)
        self.target_search_agent = TargetSearchAgent(model_name=SUB_AGENT_MODEL)
        self.source_query_execution_agent = SourceQueryExecutionAgent(model_name=SUB_AGENT_MODEL)
        self.target_query_execution_agent = TargetQueryExecutionAgent(model_name=SUB_AGENT_MODEL)
        self.validation_agent = ValidationAgent(
            model_name=SUB_AGENT_MODEL,
            source_query_agent=self.source_query_execution_agent,
            target_query_agent=self.target_query_execution_agent
        )
        self.reporting_agent = ReportingAgent(model_name=SUB_AGENT_MODEL)
        self.prompt_generator_agent = PromptGeneratorAgent(model_name=SUB_AGENT_MODEL)
        self.scheduler_agent = SchedulerAgent(model_name=SUB_AGENT_MODEL)

        super().__init__(
            model=model_name,
            name="DataValidationRootAgent",
            description="Orchestrates comprehensive data validation workflows across heterogeneous systems.",
            instruction="""You are the central coordinator for all data validation activities.
                           Your primary responsibility is to interpret high-level validation requests,
                           decompose them into manageable subtasks, and intelligently delegate these
                           subtasks to specialized sub-agents. You must maintain the overall state
                           of the validation workflow, aggregate results from all sub-agents, and
                           manage communication with the user or external systems. Always prioritize
                           data accuracy, integrity, and clear reporting of discrepancies.
                           Utilize your sub-agents effectively to achieve complete data validation.""",
            sub_agents=[
                self.source_search_agent,
                self.target_search_agent,
                self.source_query_execution_agent,
                self.target_query_execution_agent,
                self.validation_agent,
                self.reporting_agent,
                self.prompt_generator_agent,
                self.scheduler_agent,
            ],
            # Memory configuration can be added here, especially when deploying to Agent Engine:
            # session_service=..., # For short-term conversational memory
            # artifact_service=..., # For storing intermediate artifacts
            # memory_bank=... # For long-term memory via Agent Engine's managed memory
        )

    async def validate_data_integrity(self, validation_request: dict):
        """
        Initiates a data validation workflow based on a high-level request.
        The Root Agent uses its LLM capabilities to plan and orchestrate the execution
        across various sub-agents.

        Args:
            validation_request (dict): A dictionary containing details for validation, e.g.,
                                       {"source_table": "my_source_db.schema.table1",
                                        "target_table": "my_target_db.schema.table1",
                                        "validation_rules": [{"type": "count"}, {"type": "sum", "column": "amount"}]}
        """
        print(f"Root Agent received validation request: {validation_request}")

        source_table_full_name = validation_request.get("source_table")
        target_table_full_name = validation_request.get("target_table")
        validation_rules = validation_request.get("validation_rules",)

        if not source_table_full_name or not target_table_full_name or not validation_rules:
            return {"status": "failed", "message": "Missing required parameters for validation."}

        # Example of how Root Agent might orchestrate:
        # In a real scenario, the LLM would dynamically decide the sequence/parallelism
        # based on the validation_request and available tools/sub-agents.
        # ADK's WorkflowAgent (Sequential, Parallel) could be used here for more deterministic flows.

        # Step 1: (Optional) Use PromptGeneratorAgent to refine the request for LLM planning
        # This ensures the LLM receives a well-structured prompt for task decomposition.
        # For this example, we'll directly pass the request.
        # refined_prompt = await self.prompt_generator_agent.generate_validation_plan_prompt(validation_request)
        # plan = await self.llm.generate_plan(refined_prompt)

        # Step 2: Perform schema discovery using Search Agents (conceptual for now, or can be integrated into ValidationAgent)
        # For a quick test, we'll assume schema info is implicitly handled or derived by ValidationAgent.
        # print("Root Agent: Initiating schema discovery...")
        # source_schema_info = await self.source_search_agent.discover_schema(source_table_full_name)
        # target_schema_info = await self.target_search_agent.discover_schema(target_table_full_name)
        # print(f"Source Schema: {source_schema_info}, Target Schema: {target_schema_info}")

        # Step 3: Trigger validation using the Validation Agent
        print("Root Agent: Triggering data validation...")
        validation_results = await self.validation_agent.validate_data(
            source_db_name=SOURCE_DB_CONNECTION_NAME, # Use configured MCP connection name
            target_db_name=TARGET_DB_CONNECTION_NAME, # Use configured MCP connection name
            source_table=source_table_full_name,
            target_table=target_table_full_name,
            validation_rules=validation_rules
        )
        print(f"Validation Results: {validation_results}")

        # Step 4: Generate a report using the Reporting Agent
        print("Root Agent: Generating validation report...")
        report_summary = await self.reporting_agent.generate_report(validation_results)
        print(f"Report Summary: {report_summary}")

        return {"status": "Validation workflow completed", "final_report_summary": report_summary}