# Use an official Python runtime as a base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variable to disable interactive prompts (optional)
ENV PYTHONUNBUFFERED 1

# Expose the port the app runs on (if applicable)
EXPOSE 8080

# Run the pipeline script (replace with your actual script name)
CMD ["python", "src/main.py"]
