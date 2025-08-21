import os

# --- GCP Project Settings ---
# Replace with your actual GCP Project ID and Location
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
GCP_LOCATION = os.getenv("GCP_LOCATION", "us-central1")
GCP_STAGING_BUCKET = os.getenv("GCP_STAGING_BUCKET", f"gs://{GCP_PROJECT_ID}-adk-staging")

# --- MCP Toolbox Settings ---
# IMPORTANT: Replace with the actual URL and API Key of your deployed MCP Toolbox server
# We'll run MCP Toolbox on port 7000 for this example to avoid conflicts with 8080
MCP_TOOLBOX_BASE_URL = os.getenv("MCP_TOOLBOX_BASE_URL", "http://localhost:7000")
MCP_TOOLBOX_API_KEY = os.getenv("MCP_TOOLBOX_API_KEY", "your-mcp-api-key") # Use a strong, securely managed key

# --- BigQuery Settings for Persistence ---
# Replace with your BigQuery dataset and table for validation results
BIGQUERY_RESULTS_TABLE = os.getenv("BIGQUERY_RESULTS_TABLE", f"{GCP_PROJECT_ID}.data_validation_results.validation_summary")

# --- Agent Model Settings ---
# Choose appropriate Gemini models for your agents
# gemini-1.5-pro for more complex reasoning, gemini-1.5-flash for faster, cheaper tasks
ROOT_AGENT_MODEL = os.getenv("ROOT_AGENT_MODEL", "gemini-1.5-pro")
SUB_AGENT_MODEL = os.getenv("SUB_AGENT_MODEL", "gemini-1.5-flash")

# --- Memory Settings (Conceptual for local testing, managed by Agent Engine in production) ---
# For local testing, ADK uses in-memory sessions by default.
# For production on Agent Engine, these are managed automatically.
# SESSION_SERVICE_URI = os.getenv("SESSION_SERVICE_URI", None) # e.g., for Memorystore for Redis
# ARTIFACT_SERVICE_URI = os.getenv("ARTIFACT_SERVICE_URI", None) # for storing intermediate artifacts
# MEMORY_BANK_URI = os.getenv("MEMORY_BANK_URI", None) # for long-term memory (Firestore/Spanner)

# --- Example Database Connection Names for MCP Toolbox ---
# These are logical names that you would configure within your MCP Toolbox server.
# For example, in your MCP Toolbox configuration, you might define:
# connections:
#   source_gcp_mysql:
#     type: mysql
#     host:...
#   target_gcp_bigquery:
#     type: bigquery
#     project_id:...
SOURCE_DB_CONNECTION_NAME = os.getenv("SOURCE_DB_CONNECTION_NAME", "your_source_db_connection_name")
TARGET_DB_CONNECTION_NAME = os.getenv("TARGET_DB_CONNECTION_NAME", "your_target_db_connection_name")

# --- Reporting Tools Settings ---
REPORTING_EMAIL_SENDER = os.getenv("REPORTING_EMAIL_SENDER", "validation-alerts@yourcompany.com")

# --- Scheduler Tools Settings ---
# Example Firestore collection for scheduled tasks/prompts
FIRESTORE_SCHEDULE_COLLECTION = os.getenv("FIRESTORE_SCHEDULE_COLLECTION", "scheduled_validation_tasks")

# --- Prompt Generator Tools Settings ---
# Example Firestore collection for prompt templates
FIRESTORE_PROMPT_TEMPLATES_COLLECTION = os.getenv("FIRESTORE_PROMPT_TEMPLATES_COLLECTION", "prompt_templates")