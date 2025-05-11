# Makefile for fhir-pipeline

# Create a virtual environment and install runtime dependencies
install:
	@echo "Creating virtual environment and installing runtime dependencies..."
	python3 -m venv venv
	. venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Install development dependencies into the virtual environment
dev-install:
	@echo "Installing development dependencies into the virtual environment..."
	. venv/bin/activate && pip install -r requirements-dev.txt

# Run unit tests using pytest
test:
	@echo "Running tests..."
	. venv/bin/activate && PYTHONPATH=src pytest tests

# Run the main ETL pipeline
run:
	@echo "Running the FHIR pipeline..."
	. venv/bin/activate && PYTHONPATH=src python src/main.py

# Remove all .pyc files
clean:
	@echo "Cleaning up compiled Python files..."
	find . -name "*.pyc" -delete

