import os
import psycopg2


def import_csv_to_postgres():
    """Copies data from CSV files to our database
    """
    dbname = 'postgres'
    user = 'jhu'
    password = 'jhu123'  
    host = 'localhost'

    files_and_tables = {
        # '~//airflow_scripts/spos_data.csv': 'spos.data',
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