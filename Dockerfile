# Use the official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install FastAPI, Uvicorn, and pytest for running tests
RUN pip install --no-cache-dir fastapi uvicorn pytest

# Copy the FastAPI app into the container
COPY . .

# Expose port 80 for HTTP traffic
EXPOSE 80

# Run the FastAPI app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
