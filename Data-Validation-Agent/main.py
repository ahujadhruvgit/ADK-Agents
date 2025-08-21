import uvicorn
from fastapi import FastAPI
from google.adk.agents import get_fast_api_app
import vertexai
from vertexai import agent_engines

from agents.root_agent import DataValidationRootAgent
from config.settings import GCP_PROJECT_ID, GCP_LOCATION, GCP_STAGING_BUCKET

# Initialize Vertex AI SDK
try:
    vertexai.init(project=GCP_PROJECT_ID, location=GCP_LOCATION, staging_bucket=GCP_STAGING_BUCKET)
    print(f"Vertex AI SDK initialized for project: {GCP_PROJECT_ID}, location: {GCP_LOCATION}")
except Exception as e:
    print(f"Warning: Could not initialize Vertex AI SDK. This is expected if running locally without GCP credentials or for basic ADK features. Error: {e}")

# Create an instance of your Root Agent
root_agent_instance = DataValidationRootAgent()

# Wrap the ADK agent in a FastAPI application
# This exposes the agent via HTTP endpoints for Cloud Run/Agent Engine deployment
# Set web=True to enable the ADK Web UI
app = get_fast_api_app(
    root_agent_instance,
    web=True, # Enable the ADK Web UI [1]
    # You can configure session, memory, and artifact services here if not using Agent Engine's managed ones
    # session_service=...,
    # artifact_service=...,
    # memory_bank=...
)

# You can add custom FastAPI routes here if needed, e.g., for health checks or specific triggers
@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent_name": root_agent_instance.name}

if __name__ == "__main__":
    # For local development, run with Uvicorn
    print("Starting FastAPI application locally...")
    uvicorn.run(app, host="0.0.0.0", port=8080)