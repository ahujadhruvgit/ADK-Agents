from google.cloud import bigquery
from google.api_core.exceptions import GoogleAPIError
from config.settings import BIGQUERY_RESULTS_TABLE

def persist_validation_result(validation_data: dict) -> str:
    """
    Persists validation results to a BigQuery table.
    The BigQuery table schema should be designed to accommodate the structure
    of the validation_data dictionary, including nested fields if necessary.
    """
    client = bigquery.Client()
    table_id = BIGQUERY_RESULTS_TABLE

    try:
        table = client.get_table(table_id) # Ensures table exists and client has permissions
    except GoogleAPIError as e:
        return f"Error accessing BigQuery table {table_id}: {e}. Please ensure table exists and permissions are correct."

    rows_to_insert = [validation_data] # Assuming validation_data is a single dictionary for one validation run

    try:
        errors = client.insert_rows_json(table, rows_to_insert)
        if errors:
            print(f"Encountered errors while inserting rows into BigQuery: {errors}")
            return f"Failed to persist results: {errors}"
        else:
            return "Validation results persisted successfully to BigQuery."
    except Exception as e:
        return f"An unexpected error occurred during BigQuery insertion: {e}"