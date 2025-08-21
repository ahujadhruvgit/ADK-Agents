from google.adk.agents import LlmAgent
from config.settings import SUB_AGENT_MODEL, FIRESTORE_SCHEDULE_COLLECTION
from tools.scheduling_tools import retrieve_scheduled_tasks, update_task_status

class SchedulerAgent(LlmAgent):
    def __init__(self, model_name: str = SUB_AGENT_MODEL):
        super().__init__(
            model=model_name,
            name="SchedulerAgent",
            description="Manages internal scheduling and initiation of data validation workflows.",
            instruction="""You are a specialized agent responsible for managing scheduled data validation tasks.
                           You will interface with external scheduling triggers (e.g., Cloud Scheduler)
                           and an internal prompt storage database to retrieve and initiate validation workflows.
                           Your role is to ensure tasks are picked up, processed, and their status updated.""",
            tools=[retrieve_scheduled_tasks, update_task_status] # Tools added here
        )

    async def process_scheduled_task(self, task_id: str, prompt_data: dict) -> dict:
        """
        Processes a scheduled task, initiating a validation workflow.
        In a real system, this would trigger the Root Agent.

        Args:
            task_id (str): Unique identifier for the scheduled task.
            prompt_data (dict): The data/prompt associated with the scheduled task.
        Returns:
            dict: Status of the task processing.
        """
        print(f"Scheduler Agent: Processing scheduled task {task_id} with data: {prompt_data}")

        # In a full implementation, this would call the Root Agent's validate_data_integrity method
        # Example:
        # from agents.root_agent import DataValidationRootAgent
        # root_agent = DataValidationRootAgent() # Or pass an instance during init if it's a sub-agent of a higher orchestrator
        # validation_outcome = await root_agent.validate_data_integrity(prompt_data)
        # print(f"Scheduler Agent: Validation outcome for task {task_id}: {validation_outcome}")

        # Simulate task processing
        simulated_status = "COMPLETED"
        simulated_message = f"Task {task_id} processed successfully."

        # Update task status in the database
        update_status_result = await self.tools.update_task_status(
            task_id=task_id,
            status=simulated_status,
            collection_name=FIRESTORE_SCHEDULE_COLLECTION
        )
        print(f"Scheduler Agent: Task status update result: {update_status_result}")

        return {"status": simulated_status, "task_id": task_id, "message": simulated_message}

    async def fetch_and_process_due_tasks(self, current_time: str) -> dict:
        """
        Fetches tasks due at the current time and initiates their processing.
        This would typically be invoked by an external scheduler (e.g., Cloud Scheduler).

        Args:
            current_time (str): The current timestamp to check for due tasks.
        Returns:
            dict: Summary of tasks fetched and initiated.
        """
        print(f"Scheduler Agent: Checking for tasks due at {current_time}")
        due_tasks = await self.tools.retrieve_scheduled_tasks(current_time, FIRESTORE_SCHEDULE_COLLECTION)
        
        processed_tasks_summary = []
        for task in due_tasks:
            task_id = task.get("id")
            prompt_data = task.get("prompt_data")
            print(f"Scheduler Agent: Initiating processing for task {task_id}")
            # In a real scenario, this would trigger the Root Agent asynchronously
            # For this example, we'll just log it.
            processed_tasks_summary.append({"task_id": task_id, "status": "Initiated"})
            
        return {"status": "success", "tasks_initiated": processed_tasks_summary}