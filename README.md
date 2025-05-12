# FHIR Data Processing Pipeline

This project provides a pipeline to process and transform patient data in the FHIR (Fast Healthcare Interoperability Resources) format, for simplified use by analytics teams for further processing and visualisation.

---

## 📁 Project Structure

```
fhir-pipeline/
├── data/
│   ├── raw/                # Raw data received in FHIR format
│   └── processed/          # Processed data in tabular format
├── src/
│   ├── config.py           # Configuration variables
│   ├── ingestion.py        # Module to load and parse FHIR data
│   ├── transformation.py   # Module to clean and transform data
│   ├── storage.py          # Module to save data
│   └── main.py             # Main execution file for the pipeline
├── tests/
│   ├── test_transformation.py  # Unit tests for transformation logic
│   └── test_ingestion.py       # Unit tests for ingestion logic
|   ├── data/
│   ├── test_raw/                # Raw test data 
│   └── test_raw_empty/          # Empty test folder
├── Dockerfile              # Docker configuration
├── Makefile                # Simplifies common commands
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```
---

## ⚙️ Setup

Before running the pipeline, ensure you have the necessary environment and dependencies configured.

---

## 🐳 Option 1: Docker Setup (Recommended for Full Pipeline)

### Step 1: Build the Docker Image  

`make docker-build`
This creates a Docker image based on the Dockerfile.

### Step 2: Run the Pipeline in Docker
`make docker-run`
Executes the pipeline inside a container. 

### Step 3: Run Unit Tests in Docker
`make docker-test`
Runs tests using pytest inside a Docker container.

## 💻 Option 2: Local Environment (Virtualenv)
### Note: Since Docker can consume significant system resources and energy, this local test method is a more lightweight alternative for development.

### Step 1: Install Runtime Dependencies
`make install`
Creates a venv virtual environment and installs runtime dependencies.

### Step 2: Install Development Dependencies
`make dev-install`
Installs additional tools like pytest.

### Step 3: Run Unit Tests Locally
`make test`
Executes unit tests using pytest.

## 🛢 PostgreSQL Database Setup - how to access the transformed data.

The pipeline uses PostgreSQL to persist patient data. If you're using Docker, the database setup is automated via docker-compose.

### Step 1: Start the PostgreSQL Service

`docker-compose up`
This will start the database container. The DB is accessible at localhost:5432.

### Step 2: Connect to the Database

Use psql to connect:
`psql -h localhost -U testuser -d patients`

Credentials:
`User: testuser
Password: testpass
Database: testdb`

### Step 3: View Table Contents

Once inside the psql CLI:
`SELECT * FROM patients;`

Exit with:
`\q`

## 🔄 How the Pipeline Works

### 1. Ingestion
ingestion.py loads raw FHIR JSON from data/raw/.

### 2. Transformation
transformation.py:
   Renames columns
   Converts data types
   Cleans and fills missing values

### 3. Validation
Ensures required fields are present and valid.

### 4. Storage
Saves cleaned data to:
   data/processed/ as Parquet
   PostgreSQL (into patients table)

## 🧪 Running Tests

Locally: `make test`

In Docker: `make docker-test`

## 🐳 Docker Usage Summary

Build image: `make docker-build`
Run pipeline: `make docker-run`
Run tests: `make docker-test`

## 📋 Requirements

   Python 3.10+
   Docker (optional but recommended)
   Make (for task automation)

## 🧰 Docker Installation

Install Docker Desktop from the official site: [https://www.docker.com/products/docker-desktop]

## 🔧 How could this project be scaled?

- Easily configurable: Key variables such as file paths, column mappings, and table names are centralised in config.py, making it simple to adapt the pipeline to new environments or requirements.
- Supports modular expansion: Transformation logic is broken into reusable components, allowing the pipeline to be extended to process additional FHIR resource types (e.g. Condition, Observation) with minimal changes and re-using functions.
- Schema validation included: Uses Pandera for validating the structure and data types of patient records, ensuring data quality and simplifying integration with downstream systems without constant maintenance.
- Scalable for future enhancements: The codebase is designed to support scaling via orchestration tools, or distributed processing libraries like Dask or Spark if required for larger data volumes.
- Adaptable processing flow: The main() function orchestrates a clean end-to-end pipeline, which can be refactored into a dynamic, multi-resource handler to process various FHIR resource types from a config-driven loop.

## 🔧 How could this project be secured?

- Code reviews and branching: Make future changes on separate branches to then be reviewed before merging. This prevents issues when the code is automated and in production.
- Environment-based secrets: Replaces hardcoded database credentials with environment variables using os.environ, enabling secure secret management across environments.
- Safe file handling: Accepts only valid .json files and prevents path traversal attacks by sanitizing and validating input filenames.
- Log sanitisation: Avoids logging sensitive personally identifiable information such as names, IDs, or contact details, protecting data confidentiality in logs or print statements.
- Data minimisation options: Provides a foundation for adding de-identification steps depending on the data's purpose. 
- Container hardening: Encourages running containers as non-root users with read-only volumes and limited host access.
- Security testing: Supports integration of security linters and tests to catch unsafe code patterns and handle edge-case input safely.