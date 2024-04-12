import psycopg2
import json
import hashlib

class DataAccess:
    """Controls all backend data access and adheres to CRUD: Create, Read, Update, Delete."""
    
    def __init__(self):
        self.connection_params = {
            "host": "localhost",
            "port": 5432,
            "database": "default_company",
            "user": "postgres",
            "password": "spos123"
        }

    def get_bayesian_game(self, game_id):
        """Returns the last offer price and the game information.
        """
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    query = "SELECT * FROM spos.games WHERE game_id = %s"  # Parameterized %s prevents SQL injection
                    cur.execute(query, (game_id,))
                    rows = cur.fetchall()

                    # Check if any rows were returned
                    if not rows:
                        return json.dumps({'message': 'No data found for this game ID'})
                        
                    # Unpack values
                    (game_id, seller_id, buyer_agent_id, product_id, buyer_power, seller_power, buyer_reservation_price, seller_reservation_price, current_strategy) = rows[0]
        except Exception as e:
            return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})

        # Label values
        dict = {'game_id': game_id,
                'seller_id': seller_id,
                'buyer_agent_id': buyer_agent_id,
                'product_id': product_id,
                'buyer_power': buyer_power,
                'seller_power': seller_power,
                'buyer_reservation_price': buyer_reservation_price,
                'seller_reservation_price': seller_reservation_price,
                'current_strategy': current_strategy,
                }
        data = {'message': 'Data retrieved successfully', 'data': dict}

        return json.dumps(data, default=str)


    def update_bayesian_game(self, game_id, buyer_power=None, seller_power=None, buyer_reservation_price=None, seller_reservation_price=None, current_strategy=None):
        """Returns the last offer price and the game information.
        """
        query = []
        params = []

        if buyer_power is not None:
            query.append("buyer_power = %s")
            params.append(buyer_power)
        
        if seller_power is not None:
            query.append("seller_power = %s")
            params.append(seller_power)
        
        if buyer_reservation_price is not None:
            query.append("buyer_reservation_price = %s")
            params.append(buyer_reservation_price)
        
        if seller_reservation_price is not None:
            query.append("seller_reservation_price = %s")
            params.append(seller_reservation_price)
        
        if current_strategy is not None:
            query.append("current_strategy = %s")
            params.append(current_strategy)

        # If no updates provided
        if not query:
            return json.dumps({'message': 'No updates provided'})

        query = ', '.join(query)
        params.append(game_id)
        sql_query = f"UPDATE spos.games SET {query} WHERE game_id = %s;"# Parameterized %s prevents SQL injection. This should still be safe even inserting query, no user inputs inserted


        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql_query, tuple(params))

                    # Check if any rows were returned
                    if cur.rowcount == 0:
                        return json.dumps({'message': 'No data found for this game ID'})
                    
                    # Confirm changes
                    cur.execute("SELECT * FROM spos.games WHERE game_id = %s", (game_id,))
                    updated_row = cur.fetchall()
                    # Unpack values
                    (game_id, seller_id, buyer_agent_id, product_id, buyer_power, seller_power, buyer_reservation_price, seller_reservation_price, current_strategy) = updated_row[0]
        except Exception as e:
            return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})

        # Label values
        dict = {'game_id': game_id,
                'seller_id': seller_id,
                'buyer_agent_id': buyer_agent_id,
                'product_id': product_id,
                'buyer_power': buyer_power,
                'seller_power': seller_power,
                'buyer_reservation_price': buyer_reservation_price,
                'seller_reservation_price': seller_reservation_price,
                'current_strategy': current_strategy,
                }
        data = {'message': 'Data updated successfully', 'data': dict}

        return json.dumps(data, default=str)


    def add_seller(self, seller_name, seller_email):
        """ Adds a seller to the database
        """
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    query = "INSERT INTO spos.sellers (name, email) VALUES (%s, %s);"  # Parameterized %s prevents SQL injection
                    cur.execute(query, (seller_name, seller_email))
                    rows = cur.fetchall()

                    # Check if any rows were returned
                    if not rows:
                        return json.dumps({'message': 'No data found for this '})
                        
        except Exception as e:
            return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})
        
        data = {'message': 'Data added successfully', 'data': dict}
        return json.dumps(data, default=str)


    def delete_seller(self, seller_name, seller_email):
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    query = "DELETE spos.sellers WHERE name = %s AND email = %s"  # Parameterized %s prevents SQL injection
                    cur.execute(query, (seller_name, seller_email))
                    rows = cur.fetchall()

                    # Check if any rows were returned
                    if not rows:
                        return json.dumps({'message': 'No data found for this '})
                        
        except Exception as e:
            return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})
        
        data = {'message': 'Data removed successfully', 'data': dict}
        return json.dumps(data, default=str)



    def add_employee(self, employee_name, employee_id, employee_email, password):
        """ Adds a seller to the database
        """
        # Encrypt the password
        password = encrypt_password(password)
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    query = "INSERT INTO spos.buyer_agents (name, employee_id, email, password) VALUES (%s, %s, %s, %s);"  # Parameterized %s prevents SQL injection
                    cur.execute(query, (employee_name, employee_id, employee_email, password))
                    rows = cur.fetchall()

                    # Check if any rows were returned
                    if not rows:
                        return json.dumps({'message': 'No data found for this '})
                        
        except Exception as e:
            return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})
        
        data = {'message': 'Data added successfully', 'data': dict}
        return json.dumps(data, default=str)



    def delete_employee(self, employee_name, employee_id, employee_email, password):
        """Takes employee information and removes them from the database
        Args:
            employee_name
            employee_id
            employee_email
            password

        Returns:
            json: confirms completion
        """
        try:
            with psycopg2.connect(**self.connection_params) as conn:
                with conn.cursor() as cur:
                    query = "DELETE spos.buyer_agents WHERE name = %s AND employee_id = %s AND email = %s AND password = %s"  # Parameterized %s prevents SQL injection
                    cur.execute(query, (employee_name, employee_id, employee_email, password))
                    rows = cur.fetchall()

                    # Check if any rows were returned
                    if not rows:
                        return json.dumps({'message': 'No data found for this '})
        except Exception as e:
            return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})
        
        data = {'message': 'Data deleted successfully', 'data': dict}
        return json.dumps(data, default=str)




def encrypt_password(self, password):
    # Convert the password to a byte string
    byte_card = str(password).encode()    
    # Create a SHA-256 object
    sha = hashlib.sha256()
    sha.update(byte_card)
    return sha.hexdigest()


def check_password(self, provided_password, stored_hash):
    # Hash the provided password using the same method
    byte_card = str(provided_password).encode()    
    # Create a SHA-256 object
    sha = hashlib.sha256()
    sha.update(byte_card)
    check = sha.hexdigest()
    # Compare the newly hashed password with the stored hash
    return check == stored_hash





if __name__ == "__main__":

    da = DataAccess()
    
    # Test get_bayesian_game
    # game_data = da.get_bayesian_game(game_id=1)
    # game_data = json.loads(game_data)
    # print(game_data['data'])

    # Test update_bayesian_game
    data = da.update_bayesian_game(game_id=1, buyer_reservation_price= 10)
    update_data = json.loads(data)
    print(update_data)
