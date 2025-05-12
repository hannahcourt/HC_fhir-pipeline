# Makefile for fhir-pipeline

# Make commands for off-docker testing.
VENV ?= venv
PYTHON := $(VENV)/bin/python
PIP := $(VENV)/bin/pip
ACTIVATE := . $(VENV)/bin/activate

# Create a virtual environment and install runtime dependencies
install: $(VENV)/bin/activate
	@echo "Installing runtime dependencies..."
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Install development dependencies into the virtual environment
dev-install: install
	@echo "Installing development dependencies..."
	$(PIP) install -r requirements-dev.txt

# Run unit tests using pytest
test: $(VENV)/bin/activate
	@echo "Running tests..."
	PYTHONPATH=src $(PYTHON) -m pytest tests

# Create the virtual environment if not already present
$(VENV)/bin/activate:
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV)


# Docker commands for fhir-pipeline.

# Build the Docker image
docker-build:
	@echo "Building Docker image..."
	docker build -t fhir-pipeline .

# Run the pipeline in Docker 
docker-run:
	@echo "Running the FHIR pipeline in Docker..."
	docker-compose up --build

# Run the test functions
docker-test:
	@echo "Running tests inside Docker..."
	docker run --rm --name fhir-pipeline \
		-v $(PWD):/app \
		-e PYTHONPATH=/app/src \
		-w /app \
		fhir-pipeline pytest /app/tests --maxfail=5 --disable-warnings -q

# Stop the running containers
docker-stop:
	@echo "Stopping Docker containers..."
	docker-compose down

# View logs from the Docker containers
docker-logs:
	@echo "Viewing logs from Docker containers..."
	docker-compose logs -f

# Clean up Docker images and containers
docker-clean:
	@echo "Cleaning up Docker images and containers..."
	docker-compose down --volumes --rmi all


