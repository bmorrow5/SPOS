import psycopg2
import json

# CRUD
class DataAccess:
    
    def add_data(self):
        
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
        query = "INSERT INTO wiki.content (topic, title, content, num_links) VALUES (%s, %s, %s, %s)"
        
        # Commit the changes
        conn.commit()
        cur.close()
        conn.close()
    
        # Return a success message
        response = {
            'message': 'Data added successfully'
        }
        return json.dumps(response)

