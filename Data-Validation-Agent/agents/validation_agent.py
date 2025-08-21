import json
from google.adk.agents import LlmAgent
from tools.persistence_tools import persist_validation_result
from agents.query_execution_agent import SourceQueryExecutionAgent, TargetQueryExecutionAgent
from config.settings import SUB_AGENT_MODEL

class ValidationAgent(LlmAgent):
    source_query_agent: SourceQueryExecutionAgent
    target_query_agent: TargetQueryExecutionAgent

    def __init__(self,
                 model_name: str = SUB_AGENT_MODEL,
                 source_query_agent: SourceQueryExecutionAgent = None,
                 target_query_agent: TargetQueryExecutionAgent = None):
        super().__init__(
            model=model_name,
            name="ValidationAgent",
            description="Performs data comparison and identifies discrepancies using custom logic.",
            instruction="""You are an expert data validator specializing in cross-system data integrity checks.
                           Your primary function is to retrieve data from source and target systems using
                           the Query Execution Agents and then apply custom validation rules to identify discrepancies.
                           You must accurately identify discrepancies and ensure all validation results are persisted.
                           When encountering complex scenarios, you may consult the knowledge base for historical
                           validation patterns and remediation advice.""",
            tools=[persist_validation_result],
            source_query_agent=source_query_agent,
            target_query_agent=target_query_agent
        )
        if not source_query_agent or not target_query_agent:
            raise ValueError("Source and Target Query Execution Agents must be provided to ValidationAgent.")

    async def validate_data(self, source_db_name: str, target_db_name: str, source_table: str, target_table: str, validation_rules: list) -> dict:
        """
        Performs data validation based on specified rules by querying source and target databases.

        Args:
            source_db_name (str): The logical name of the source database connection (as configured in MCP Toolbox).
            target_db_name (str): The logical name of the target database connection (as configured in MCP Toolbox).
            source_table (str): The full name of the source table to validate (e.g., 'my_dataset.my_table').
            target_table (str): The full name of the target table to validate (e.g., 'my_dataset.my_table').
            validation_rules (list): A list of dictionaries, each specifying a validation rule.
                                     Example: [{"type": "count"}, {"type": "sum", "column": "amount"}]
        Returns:
            dict: A summary of the validation status and results.
        """
        print(f"Validation Agent: Running custom validation for {source_table} vs {target_table}")
        overall_status = "SUCCESS"
        discrepancies = []
        detailed_results = []

        for rule in validation_rules:
            rule_type = rule.get("type")
            result = {"rule_type": rule_type, "status": "UNKNOWN", "details": {}}

            try:
                if rule_type == "count":
                    source_count_query = f"SELECT COUNT(*) FROM {source_table}"
                    target_count_query = f"SELECT COUNT(*) FROM {target_table}"

                    source_count_res = await self.source_query_agent.execute_query(source_count_query, source_db_name)
                    target_count_res = await self.target_query_agent.execute_query(target_count_query, target_db_name)

                    # Extract count from results. Assuming result format {"columns": ["count"], "rows": []}
                    source_count = source_count_res.get("data", {}).get("rows", [[None]]) if source_count_res.get("data", {}).get("rows") else None
                    target_count = target_count_res.get("data", {}).get("rows", [[None]]) if target_count_res.get("data", {}).get("rows") else None

                    if source_count is not None and target_count is not None and source_count == target_count:
                        result["status"] = "SUCCESS"
                    else:
                        result["status"] = "FAIL"
                        overall_status = "FAIL"
                        result["details"] = {"source_count": source_count, "target_count": target_count, "message": "Row counts do not match."}
                    print(f"  Count Validation: Source={source_count}, Target={target_count}, Status={result['status']}")

                elif rule_type == "sum":
                    column = rule.get("column")
                    if not column:
                        raise ValueError("Column must be specified for 'sum' validation.")
                    source_sum_query = f"SELECT SUM({column}) FROM {source_table}"
                    target_sum_query = f"SELECT SUM({column}) FROM {target_table}"

                    source_sum_res = await self.source_query_agent.execute_query(source_sum_query, source_db_name)
                    target_sum_res = await self.target_query_agent.execute_query(target_sum_query, target_db_name)

                    # Extract sum from results. Assuming result format {"columns": ["sum"], "rows": [[123.45]]}
                    source_sum = source_sum_res.get("data", {}).get("rows", [[None]]) if source_sum_res.get("data", {}).get("rows") else None
                    target_sum = target_sum_res.get("data", {}).get("rows", [[None]]) if target_sum_res.get("data", {}).get("rows") else None

                    if source_sum is not None and target_sum is not None and source_sum == target_sum:
                        result["status"] = "SUCCESS"
                    else:
                        result["status"] = "FAIL"
                        overall_status = "FAIL"
                        result["details"] = {"column": column, "source_sum": source_sum, "target_sum": target_sum, "message": f"Sum of column '{column}' does not match."}
                    print(f"  Sum Validation ({column}): Source={source_sum}, Target={target_sum}, Status={result['status']}")

                elif rule_type == "schema":
                    # This is a simplified example. Real schema comparison is complex and database-specific.
                    # For BigQuery, you might query `INFORMATION_SCHEMA.COLUMNS` directly.
                    # For other databases, adjust the query accordingly.
                    # This query assumes a database with INFORMATION_SCHEMA like MySQL or PostgreSQL.
                    source_schema_query = f"""
                    SELECT column_name, data_type, is_nullable
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE table_name = '{source_table.split('.')[-1]}'
                    ORDER BY column_name;
                    """
                    target_schema_query = f"""
                    SELECT column_name, data_type, is_nullable
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE table_name = '{target_table.split('.')[-1]}'
                    ORDER BY column_name;
                    """

                    source_schema_res = await self.source_query_agent.execute_query(source_schema_query, source_db_name)
                    target_schema_res = await self.target_query_agent.execute_query(target_schema_query, target_db_name)

                    source_schema = source_schema_res.get("data", {}).get("rows",)
                    target_schema = target_schema_res.get("data", {}).get("rows",)

                    # Convert to a comparable format (e.g., list of dicts)
                    source_schema_parsed = []
                    if source_schema_res.get("data", {}).get("columns"):
                        cols = source_schema_res["data"]["columns"]
                        for row in source_schema:
                            source_schema_parsed.append({cols[i]: row[i] for i in range(len(cols))})

                    target_schema_parsed = []
                    if target_schema_res.get("data", {}).get("columns"):
                        cols = target_schema_res["data"]["columns"]
                        for row in target_schema:
                            target_schema_parsed.append({cols[i]: row[i] for i in range(len(cols))})

                    # Sort by column_name for consistent comparison
                    if sorted(source_schema_parsed, key=lambda x: x.get('column_name', '')) == sorted(target_schema_parsed, key=lambda x: x.get('column_name', '')):
                        result["status"] = "SUCCESS"
                    else:
                        result["status"] = "FAIL"
                        overall_status = "FAIL"
                        result["details"] = {"source_schema": source_schema_parsed, "target_schema": target_schema_parsed, "message": "Schemas do not match."}
                    print(f"  Schema Validation: Status={result['status']}")

                # Add more custom validation types (e.g., row-level hash, custom query) here
                # For row-level hash, you'd fetch all rows, concatenate relevant columns, hash them, and compare hashes.
                # This can be memory intensive for large tables.
                # Example:
                # elif rule_type == "row_hash":
                #     # Fetch all rows from source and target, compute hash, compare
                #     source_rows_query = f"SELECT * FROM {source_table} ORDER BY <primary_key_column>"
                #     target_rows_query = f"SELECT * FROM {target_table} ORDER BY <primary_key_column>"
                #     source_data = await self.source_query_agent.execute_query(source_rows_query, source_db_name)
                #     target_data = await self.target_query_agent.execute_query(target_rows_query, target_db_name)
                #     # Implement hashing and comparison logic here
                #...

                else:
                    result["status"] = "ERROR"
                    result["details"] = {"message": f"Unsupported validation rule type: {rule_type}"}
                    overall_status = "ERROR"

            except Exception as e:
                result["status"] = "ERROR"
                result["details"] = {"message": f"Error during {rule_type} validation: {str(e)}"}
                overall_status = "FAIL" 
                print(f"  Error during {rule_type} validation: {e}")

            detailed_results.append(result)
            if result["status"] in detailed_results: 
                discrepancies.append(result)

        validation_summary = {
            "overall_status": overall_status,
            "total_rules_run": len(validation_rules),
            "total_discrepancies": len(discrepancies),
            "detailed_results": detailed_results
        }

        # Persist results using the persistence tool
        persistence_status = await persist_validation_result(validation_summary)
        print(f"Validation Agent: Persistence status: {persistence_status}")

        # Optional: Query KB for insights on discrepancies if validation_summary indicates failures
        # if overall_status == 'FAIL' and discrepancies:
        #     relevant_kb_info = await vector_search_kb.query_semantic_info(json.dumps(discrepancies))
        #     print(f"Validation Agent: KB insights: {relevant_kb_info}")
        #     validation_summary['kb_insights'] = relevant_kb_info

        return {"status": "completed", "summary": validation_summary, "persistence_status": persistence_status}