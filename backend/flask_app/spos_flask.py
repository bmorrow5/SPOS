from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
import requests
import json
import time

app = Flask(__name__)



"""
Ignore the below this is old code I am modifying from an old project I did, and am using this as a template
"""



# Define an empty DataFrame
df = pd.DataFrame(columns=['topic', 'title', 'content', 'num_links'])

# Accepts a json topic, scrapes wikipedia for it, returns the scraped data, and adds it to Flask DataFrame
@app.route('/api/scrape_topic', methods=['POST'])
def scrape_topic():

    # Get the data from the request body
    topic = request.json['topic']
    url = f'https://en.wikipedia.org/wiki/{topic}'
    
    try:
        # Get the page content and error handling
        response = requests.get(url)
        response.raise_for_status()  # raise HTTPError for 4xx and 5xx status codes
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get the title, first 100 characters, and number of links
        title = soup.find('title').text 
        first_100_char = soup.find('p').text.strip()[0:100]
        links = []
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        num_links = len(links) 
        
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:
            print('Rate limit exceeded. Waiting for 60 seconds...')
            time.sleep(60)
        else:
            print(f'HTTP error occurred: {err}')
    except requests.exceptions.RequestException as err:
        print(f'Request error occurred: {err}')
    except (AttributeError, TypeError) as err: 
        print(f'Parsing error occurred: {err}') 
    else:
        print('Page scrapped successfully!')
    
    # Return the data as a JSON object
    response = {
        'topic': topic, 
        'title': title,  
        'content': first_100_char, 
        'num_links': num_links
    }    

    # Also save data to flask DataFrame
    global df
    df = pd.concat([df, pd.DataFrame([response])], ignore_index=True)

    return jsonify(response)

# A DELETE endpoint to delete data from the DataFrame
@app.route('/api/delete_data', methods=['DELETE'])
def delete_data():
    topic = request.json['topic']  # Get the name from the request body
    
    global df
    df = df[df['topic'] != topic]  # Delete the data from the DataFrame

    # Return a success message
    response = {
        'message': 'Data deleted successfully',
	'data': df.to_dict()
    }
    return jsonify(response)

# A PUT endpoint to update data in the DataFrame
@app.route('/api/update_data', methods=['PUT'])
def update_data():
    # Get the data from the request body
    data = request.json

    # Update the title, content, num_links for the given topic
    global df
    df.loc[df['topic'] == data['topic'], 'title'] = data['title']
    df.loc[df['topic'] == data['topic'], 'content'] = data['content']
    df.loc[df['topic'] == data['topic'], 'num_links'] = data['num_links']

    # Return a success message
    response = {
        'message': 'Data updated successfully',
        'data': df.to_dict()
    }
    return jsonify(response)

# Saves all records of the data to a PostgreSQL database
@app.route('/api/add_to_database', methods=['GET'])
def add_to_database():
    
    ## Connect to Database
    conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="jhu",
    user="postgres",
    password="jhu123")
    
    # Create Schema and Table
    cur = conn.cursor()
    cur.execute(
        """
        CREATE SCHEMA IF NOT EXISTS wiki
        """)
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS wiki.content (
                    id SERIAL PRIMARY KEY,
                    topic VARCHAR(256) NOT NULL,
                    title VARCHAR(256) NOT NULL,
                    content VARCHAR(100) NOT NULL,
                    num_links INTEGER)
        """)
    
    # Insert Data
    ## NOTE: Use bound variables, never string formatting to prevent SQL Injection
    query = "INSERT INTO wiki.content (topic, title, content, num_links) VALUES (%s, %s, %s, %s)"
    global df
    data = [tuple(row) for row in df[['topic', 'title', 'content', 'num_links']].values]
    cur.executemany(query, data)

    # Commit the changes
    conn.commit()
    cur.close()
    conn.close()
    
    # Return a success message
    response = {
        'message': 'Data added successfully'
    }
    return jsonify(response)

# View all records in postgresql database
@app.route('/api/view_database', methods=['GET'])
def view_database():
    
    ## Connect to Database
    conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="jhu",
    user="postgres",
    password="jhu123")
    
    # Display table
    cur = conn.cursor()
    cur.execute("SELECT * FROM wiki.content;")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    # Return a success message
    response = {
        'message': 'Database found. Contents:',
        'data': rows
    }
    return jsonify(response)


# Define a GET endpoint to retrieve all data from the DataFrame
@app.route('/api/get_data', methods=['GET'])
def get_data():
    # Return the data as a JSON object
    data = df.to_dict()
    return jsonify(data) 


if __name__ == '__main__':
    port=8001
    app.run(debug=True, port=port)

