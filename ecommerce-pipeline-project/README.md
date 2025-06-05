# E-commerce Data Pipeline Project

This project contains scripts for processing and analyzing e-commerce data, orchestrated using Apache Airflow.

## Project Structure

```
ecommerce-pipeline-project/
├── data/               # Directory containing CSV data files
├── dags/              # Airflow DAG definitions
│   └── ecommerce_pipeline_dag.py
├── extract/           # Data extraction scripts
│   └── extract.py     # Script to analyze CSV files
├── airflow.cfg        # Airflow configuration
├── requirements.txt   # Project dependencies
└── README.md         # This documentation file
```

## Setup

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize Airflow:
```bash
# Set Airflow home
export AIRFLOW_HOME=$(pwd)  # On Windows: set AIRFLOW_HOME=%CD%

# Initialize the database
airflow db init

# Create an admin user
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
```

## Running the Pipeline

1. Start the Airflow webserver:
```bash
airflow webserver --port 8080
```

2. In a new terminal, start the Airflow scheduler:
```bash
airflow scheduler
```

3. Access the Airflow UI at http://localhost:8080
   - Login with username: admin, password: admin
   - Enable the 'ecommerce_pipeline' DAG
   - Trigger the DAG manually or wait for the scheduled run

## Extract Script

The `extract.py` script analyzes CSV files in the `data` directory and provides a summary of their contents.

### Features

- Scans all CSV files in the data directory
- Provides summary statistics for each file:
  - Number of rows
  - Number of columns
  - File name
- Handles errors gracefully if files cannot be read
- Colored logging using rich library
- Modular structure with separate functions

### Usage

1. Place your CSV files in the `data` directory
2. Run the script:
```bash
python extract/extract.py
```

### Output

The script will display a table showing:
- File name
- Number of rows
- Number of columns
- Any errors encountered while reading the file

Example output format:
```
file_name    num_rows    num_columns
data1.csv    1000       15
data2.csv    500        8
```

### Requirements

- Python 3.x
- pandas library
- rich library
- Apache Airflow (for orchestration)

### Installation

Install the required dependencies:
```bash
pip install pandas
```
