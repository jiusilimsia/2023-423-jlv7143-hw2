# This Dockerfile defines the setup for running the cloud classification pipeline.

# 1. Use the official Python 3.10.9-slim base image (for a minimal and lightweight setup)
FROM python:3.10.9-slim

# 2. Set the working directory to /app (which will contain all application files)
WORKDIR /app

# 3. Copy the requirements.txt file into the container and install the dependencies using pip.
COPY requirements.txt .
RUN pip install -r requirements.txt

# 4. Copy the config directory, src directory, and pipeline.py file into the container.  (ensures the application code and configuration files are available within the container)
COPY config config/
COPY src src/
COPY pipeline.py .

# 5. Set the default command (CMD) to execute the pipeline.py script using Python.
CMD ["python", "pipeline.py"]
