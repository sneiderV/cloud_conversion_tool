# Use an official Python runtime as the base image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /conversion_app

# Copy the rest of the application code to the container
COPY . .

# Install the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Set environment variables
#ENV FLASK_APP="conversion_app"
#ENV FLASK_DEBUG=1
#ENV FLASK_ENV=development

# Expose port 9876 for the Flask development server to listen on
EXPOSE 9876

# Define the command to run the Flask development server
CMD ["flask", "run", "--host=0.0.0.0", "-p 9876"]