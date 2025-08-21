import uvicorn
from fastapi import FastAPI
from google.adk.cli.fast_api import get_fast_api_app
from google.adk.agents import Agent

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

# Create the FastAPI application without passing the agent
app = get_fast_api_app(web=True,agents_dir="agents")

# Register the agent with the application after its creation
app.agent = root_agent_instance

# You can add custom FastAPI routes here if needed, e.g., for health checks or specific triggers
@app.get("/health")
async def health_check():
    return {"status": "healthy", "agent_name": app.agent.name}

if __name__ == "__main__":
    # For local development, run with Uvicorn
    print("Starting FastAPI application locally...")
    uvicorn.run(app, host="0.0.0.0", port=8080)