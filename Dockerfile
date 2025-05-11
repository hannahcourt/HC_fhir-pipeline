# Use an official lightweight Python image
FROM python:3.10-slim

# Set working directory in the container
WORKDIR /app

# Copy the current project into the container
COPY . .

# Install runtime dependencies (this includes both runtime and dev dependencies)
RUN pip install --upgrade pip && pip install -r requirements.txt

# Create data directories (optional safety)
RUN mkdir -p data/raw data/processed

# Default command to run the pipeline
# This can be overridden when running tests, so it doesn't conflict
CMD ["python", "src/main.py"]




