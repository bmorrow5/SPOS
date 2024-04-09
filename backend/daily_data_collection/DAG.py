import time
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta
from airflow.utils.trigger_rule import TriggerRule
import subprocess


# Define the default arguments
default_args = {
	'owner': 'data_engineer',
	'start_date': datetime(2023, 4, 6),
	'retries': 1,
	'retry_delay': timedelta(minutes=1)
}

# Define the DAG
with DAG('process_student_data', default_args=default_args, schedule_interval='@daily') as dag:


	# start_flask_api_task = PythonOperator(
    # 		task_id="start_flask_api",
    # 		python_callable=start_flask_api,
    # 		dag=dag
	# 	)
	end_dag_task = DummyOperator(
		task_id = "end_dag",
		dag=dag
	)

	# Load data daily
	start_flask_api_task >> end_dag_task
	