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
`psql -h localhost -U fhiruser -d patients`

Credentials:
`User: fhiruser
Password: password
Database: patients`

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

