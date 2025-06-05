from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import sys
import os

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract.extract import main as extract_main

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'ecommerce_pipeline',
    default_args=default_args,
    description='E-commerce data pipeline for processing CSV files',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    catchup=False,
    tags=['ecommerce', 'data-pipeline'],
)

# Define tasks
extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_main,
    dag=dag,
)

# Set task dependencies
extract_task  # This is our only task for now, but we can add more tasks later 