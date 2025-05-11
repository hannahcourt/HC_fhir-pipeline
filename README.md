FHIR Data Processing Pipeline

This project provides a pipeline to process and transform patient data in the FHIR (Fast Healthcare Interoperability Resources) format. The transformed data is saved in a more structured and accessible format, such as Parquet, to be used by analytics teams for further processing and visualisation.

Project Structure:

fhir-pipeline/
├── data/
│   ├── raw/          # Raw data received in FHIR format
│   └── processed/    # Processed data in tabular format
├── src/
│   ├── config.py     # Configuration variables
│   ├── ingestion.py  # Module to load and parse FHIR data
│   ├── transformation.py # Module to clean and transform data
│   ├── storage.py    # Module to save data
│   └── main.py       # Main execution file for the pipeline
├── tests/
│   ├── test_transformation.py # Unit tests for the transformation logic
│   └── test_ingestion.py     # Unit tests for the ingestion logic
├── Dockerfile        # Docker configuration for containerizing the pipeline
├── Makefile          # Makefile to simplify common commands
├── requirements.txt  # Python dependencies
└── README.md         # Project documentation
Setup

Before running the pipeline, ensure you have the necessary environment and dependencies set up.

Option 1: Set Up Docker Environment
This project supports Docker to containerize the pipeline and its dependencies for easy deployment and execution.

    Step 1: Build the Docker Image
        To build the Docker image, use:

            - `make docker-build`
            - This will create a Docker image based on the Dockerfile, allowing you to run the pipeline in a containerized environment.

    Step 2: Run the Pipeline in Docker
        To run the pipeline inside the Docker container, use:

            - `make docker-run`
            - This will start the Docker container and execute the pipeline inside it. The data/ directory is mounted into the container, so processed data will be saved to the local data/processed/ directory.

    Step 3: Run Unit Tests in Docker
        To run the tests inside the Docker container, use:

            - `make docker-test`
            - This will run the tests defined in the tests/ directory using pytest.

Option 2: Set Up Local Environment (Virtual Environment)
If you prefer to work locally (without Docker), you can set up a Python virtual environment to run the pipeline and tests.

    Step 1: Install Runtime Dependencies
        To create a virtual environment and install the main dependencies, use:

            - `make install`
            - This will create a virtual environment called venv and install the necessary runtime dependencies from requirements.txt.

    Step 2: Install Development Dependencies
        If you need additional development dependencies (e.g., for testing with pytest or pytest-docker), use:

            - `make dev-install`

    Step 3: Run Unit Tests Locally
        To run the unit tests in your local environment, use:

            - `make test`
            - This will execute the tests from the tests/ directory.

    Step 4: Run the Pipeline Locally
        To run the pipeline locally, use:

           - `make run`
            - This will execute the main pipeline using python src/main.py.

PostgreSQL Database Setup:

The pipeline uses PostgreSQL to store patient data, and Docker will manage the database for you.

Docker PostgreSQL Setup:
If you are using Docker, the PostgreSQL database will be set up automatically. The configuration is defined in the docker-compose.yml file.

Step 1: Start the PostgreSQL Database
Once you have the Docker containers running (via docker-compose up), the PostgreSQL database will be accessible on localhost:5432.

Accessing the Database:

Step 1: Connect to the Database
To connect to the database, you can use the psql command-line client. By default, the PostgreSQL database runs with the following credentials:

    User: fhiruser
    Password: password
    Database: patients

Run the following command in your terminal:
- `psql -h localhost -U fhiruser -d patients`

You will be prompted for the password. Enter password to authenticate.

Step 2: Inspect the Data
Once connected to the PostgreSQL database, you can inspect the data stored in the patients table by running the following SQL commands:

View all records in the patients table:
- `SELECT * FROM patients;`
You can also run other SQL queries to analyse or manipulate the data.

Exit the table:
- `\q`

Troubleshooting Database Connection:
If you encounter issues connecting to the database, ensure that the Docker containers are running with:

- `docker-compose up`
You may need to restart the Docker containers if changes are made to the PostgreSQL service.

How the Pipeline Works:

The pipeline follows these steps:
    Ingestion: The ingestion.py module loads raw FHIR data from the data/raw/ directory.
    Transformation: The transformation.py module processes the data by:
    Renaming columns for easier understanding.
    Converting data types where necessary.
    Cleaning and filling missing values.
    Validation: The pipeline validates the data to ensure all required fields are present and the data is consistent.
    Storage: The processed data is saved in the data/processed/ directory, typically in the Parquet format for better compatibility with analytics tools.
    Running Tests

To ensure that everything is working correctly and the transformations behave as expected, you can run the unit tests:

Local Tests
To run tests in your local virtual environment:

- `make test`
- This will run all unit tests defined in the tests/ directory.

Docker Tests
To run tests inside Docker:

- `make docker-test`
- This will execute the tests inside the Docker container, ensuring that your environment is correctly set up for deployment.

Docker Usage

If you'd like to run the pipeline within a Docker container (for reproducibility or deployment), follow these steps:

Step 1: Build the Docker Image
- `make docker-build`
- This will create a Docker image with all required dependencies.

Step 2: Run the Pipeline in Docker
- `make docker-run`
- This will execute the pipeline inside a containerized environment, ensuring all dependencies are isolated and managed.

Requirements:

- Python 3.10 or higher
- Docker (optional for running the pipeline in a container)
- Make (optional for automating common tasks)

Optional: Docker Installation
If you plan to use Docker for running the pipeline, you'll need Docker installed on your machine. You can install Docker from the official Docker website linked here: [https://www.docker.com/products/docker-desktop/]



