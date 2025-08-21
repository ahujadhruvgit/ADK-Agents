# Use an official Python runtime as a parent image
FROM python:3.10-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for some Python packages (e.g., psycopg2-binary for PostgreSQL)
# This might need to be adjusted based on the specific databases your MCP Toolbox connects to.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container
COPY requirements.txt.

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY..

# Expose the port the app runs on
EXPOSE 8080

# Run the FastAPI application using Uvicorn
# The --host 0.0.0.0 is crucial for Cloud Run
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]