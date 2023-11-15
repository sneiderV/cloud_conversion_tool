# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /worker

# Copy the rest of the application code to the container
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
    
#CMD ["celery", "-A", "worker", "worker", "-l", "info", "-Q", "process_task_converter"]
CMD ["python", "subscriber_script.py"]