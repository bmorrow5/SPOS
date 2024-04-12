import psycopg2
import json

class DataAccess():
    """ Controls all backend data access and adheres to RUD: Read, Update, Delete
    """
    def __init__(self):
        self.connection.params = {
            "host": "localhost",
            "port": 5432,
            "database": "default_company",
            "user": "postgres",
            "password": "spos123"
        }
        self.valid_tables = ["email_logs", "sellers", "buyer_agents", "products", "games"]  # Whitelist of tables


    def read(self, table, column_id) -> json:
        """Connects and reads data from the database
        """
        # Connect to database
        try:
            conn = psycopg2.connect(self.connection_params)
        except:
            print(f"I am unable to connect to the database")
    
        cur = conn.cursor()
        
        # Insert Data
        # Use parameterized queries to prevent SQL injection https://www.psycopg.org/docs/usage.html#passing-parameters-to-sql-queries
        query = "SELECT * FROM spos.buyer_agents"
        data = ('*',)
        cur.execute(query)
        rows = cur.fetchall()

        # Commit the changes
        conn.commit()
        cur.close()
        conn.close()
    
        # Return a success message
        response = {
            'message': 'Data added successfully',
            'data': rows
        }
        return json.dumps(response, default=str)




    def update(self, record_to_update, id_column) -> json:

        # Connect to database
        try:
            conn = psycopg2.connect(self.connection_params)
        except:
            print(f"I am unable to connect to the database")
    
        cur = conn.cursor()
        ## NOTE: Use bound variables, never string formatting to prevent SQL Injection

        query = "INSERT INTO spos (topic, title, content, num_links) VALUES (%s, %s, %s, %s)"

        # Insert Data
        for record in record_to_update:
            cur.execute(query, record)
        rows = cur.fetchall()


        # Commit the changes
        conn.commit()
        cur.close()
        conn.close()
    
        # Return a success message
        response = {
            'message': 'Data added successfully',
            'data': rows
        }
        return json.dumps(response, default=str)
    

    def delete(self, table) -> json:
        
        # Connect to Database
        conn = psycopg2.connect(
        host="localhost",
        port=5432,
        database="jhu",
        user="postgres",
        password="jhu123")
    
        cur = conn.cursor()

        # Insert Data
        ## NOTE: Use bound variables, never string formatting to prevent SQL Injection
        query = "INSERT INTO spos (topic, title, content, num_links) VALUES (%s, %s, %s, %s)"
        cur.execute(query)
        rows = cur.fetchall()


        # Commit the changes
        conn.commit()
        cur.close()
        conn.close()
    
        # Return a success message
        response = {
            'message': 'Data added successfully',
            'data': rows
        }
        return json.dumps(response, default=str)
    


if __name__ == "main":
    json = DataAccess.read()

    data = json['data']
    print(json)
    print("test")
    print(data)

