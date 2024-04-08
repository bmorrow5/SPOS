import os
import psycopg2

""" This code will insert the updated data into the database.
"""


def import_csv_to_postgres():
    dbname = 'postgres'
    user = 'jhu'
    password = 'jhu123'  
    host = 'localhost'

    files_and_tables = {
        '~/EN.685.648.81.FA23-main/airflow_scripts/economic_indicators.csv': 'covid.economic_indicators',
        '~/EN.685.648.81.FA23-main/airflow_scripts/emissions_data.csv': 'covid.emissions_data',
        '~/EN.685.648.81.FA23-main/airflow_scripts/COVID-19_Case_Surveillance_Public_clean.csv': 'covid.covid_data',
        '~/EN.685.648.81.FA23-main/airflow_scripts/spy_data.csv': 'covid.stock_data'
    }

    # Connect to the database
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    cur = conn.cursor()

    for file_path, table in files_and_tables.items():
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                cur.copy_expert(f"COPY {table} FROM stdin WITH CSV HEADER NULL AS 'NA'", f)
            conn.commit()
            print(f"Data from {file_path} imported into {table}")
        else:
            print(f"File {file_path} not found, skipping import for {table}")

    cur.close()
    conn.close()