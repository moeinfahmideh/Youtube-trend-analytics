import os
from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta
PROJECT_DIR = "/Users/moeinfahmide/Desktop/Job/Learning/Data Engineering/projects/youtube"
DBT_PROJECT_DIR = f"{PROJECT_DIR}/youtube_dbt"
PROFILES_DIR   = PROJECT_DIR 
# Default arguments for retries, owner, etc.
default_args = {
    'owner': 'you',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    dag_id='youtube_daily_pipeline',
    default_args=default_args,
    description='Ingest YouTube data and run dbt daily',
    start_date=datetime(2025, 5, 12),
    schedule_interval='50 21 * * *',
    catchup=False,
) as dag:


    # 1) Ingest raw data
    popular_ingest = BashOperator(
        task_id='popular_ingest',
        bash_command=f'cd "{PROJECT_DIR}" && python ingestion/popular_ingest.py',
    )

    # 2) Run dbt models
    dbt_run = BashOperator(
        task_id='dbt_run',
        bash_command=(
            f'cd "{DBT_PROJECT_DIR}" && '
            f'dbt run '
            f'--project-dir "{DBT_PROJECT_DIR}" '
            f'--profiles-dir "{PROFILES_DIR}" '
            '--models staging+ marts+'
        ),
    )
    

    
    

    # Set task order
    popular_ingest >> dbt_run 
