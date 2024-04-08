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

	load_epa_task = BashOperator(
			task_id="load_epa",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_epa.py",
			dag=dag
		)
	load_cdc_task = BashOperator(
			task_id="load_cdc",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_cdc.py",
			dag=dag
		)
	load_stock_task = BashOperator(
			task_id="load_stock",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_stock.py",
			dag=dag
		)
	load_economic_task = BashOperator(
			task_id="load_economic",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/load_economic.py",
			dag=dag
		)
	update_database_task = BashOperator(
			task_id="update_database",
			bash_command="python ~/EN.685.648.81.FA23-main/airflow_scripts/update_database.py",
			dag=dag,
		)
	start_flask_api_task = PythonOperator(
    		task_id="start_flask_api",
    		python_callable=start_flask_api,
    		dag=dag
		)
	generate_report_task = BashOperator(
		task_id = "generate_report",
		bash_command = "python ~/EN.685.648.81.FA23-main/api/report.py",
		dag=dag
	)

	# Execute loading tasks simultaneously
	[load_epa_task, load_cdc_task, load_stock_task, load_economic_task] >> update_database_task  >> start_flask_api_task >> generate_report_task
	