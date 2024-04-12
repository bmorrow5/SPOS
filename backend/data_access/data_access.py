import psycopg2
import json

class DataAccess:
    """ Controls all data access and adheres to CRUD: Create, Read, Update, Delete
    """

    def read_database(self):
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
        query = "SELECT * FROM spos"
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

    def update_database(self, table):
        
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
    json = DataAccess.read_database()

    data = json['data']
    print(data)

