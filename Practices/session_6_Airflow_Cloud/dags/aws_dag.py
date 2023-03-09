from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from datetime import datetime, timedelta
import json

# Define the DAG parameters
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 3, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1
}

def extract_data(s3_bucket_name, s3_key_name, aws_conn_id):
    print("Starting extraction")
    print("Connecting to S3")
    s3Hook = S3Hook(aws_conn_id=aws_conn_id)
    print("Airflow S3Hook connected to S3")
    return s3Hook.read_key(s3_key_name, s3_bucket_name)

def transform_data(input_json):
    print("Starting transformation")
    data = json.loads(input_json)
    csv_string = 'user_id, x_coordinate, y_coordinate, date\n'
    for row in data:
        csv_string += f'{row["user_id"]}, {row["x_coordinate"]}, {row["y_coordinate"]}, {row["date"]}\n'
    return csv_string

def load_data(csv_string, s3_bucket_name, aws_conn_id):
    print("Starting loading")
    s3Hook = S3Hook(aws_conn_id = aws_conn_id)
    s3Hook.load_string(
        csv_string,
        key = "output.csv",
        bucket_name = s3_bucket_name,
        replace = True
    )
    print("CSV was written to S3")


aws_dag = DAG('aws_dag', default_args = default_args, schedule_interval = timedelta(days = 1))

bucket_name = 's3-enroute-arturo-public-bucket'

extract_data_task = PythonOperator(
    task_id = 'extract_data',
    python_callable = extract_data,
    op_kwargs = {
        's3_bucket_name': bucket_name,
        's3_key_name': 'input.json',
        'aws_conn_id': 'aws_conn'
    },
    dag = aws_dag,
)

transform_data_task = PythonOperator(
    task_id = 'transform_data',
    python_callable = transform_data,
    op_kwargs = {
        'input_json': "{{ task_instance.xcom_pull(task_ids = 'extract_data', key = 'return_value') }}"
    },
    dag = aws_dag
)

load_data_task = PythonOperator(
    task_id = 'load_data',
    python_callable = load_data,
    op_kwargs = {
        'csv_string': "{{ task_instance.xcom_pull(task_ids = 'transform_data', key = 'return_value') }}",
        's3_bucket_name': bucket_name,
        'aws_conn_id': 'aws_conn'
    },
    dag = aws_dag
)

extract_data_task >> transform_data_task >> load_data_task