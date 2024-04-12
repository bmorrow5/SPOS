import psycopg2
import json

class DataAccess:
    """Controls all backend data access and adheres to RUD: Read, Update, Delete."""
    
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












    # def read(self, table, column_id):
    #     """Reads data from the specified table"""
    #     if table not in ["email_logs", "sellers", "buyer_agents", "products", "games"]:
    #         return json.dumps({'message': 'Invalid table name'})

    #     try:
    #         with psycopg2.connect(**self.connection_params) as conn:
    #             with conn.cursor() as cur:
    #                 query = f"SELECT * FROM {table} WHERE id = %s"
    #                 cur.execute(query, (column_id,))
    #                 rows = cur.fetchall()
    #     except Exception as e:
    #         return json.dumps({'message': 'Error connecting to the database', 'error': str(e)})

    #     return json.dumps({'message': 'Data retrieved successfully', 'data': rows}, default=str)

    # def update(self, table, id_column, update_values):
    #     """Updates a record in the specified table"""
    #     if table not in ["email_logs", "sellers", "buyer_agents", "products", "games"]:
    #         return json.dumps({'message': 'Invalid table name'})

    #     try:
    #         with psycopg2.connect(**self.connection_params) as conn:
    #             with conn.cursor() as cur:
    #                 # Example update query:
    #                 columns = ', '.join([f"{k} = %s" for k in update_values.keys()])
    #                 values = list(update_values.values()) + [id_column]
    #                 query = f"UPDATE {table} SET {columns} WHERE id = %s"
    #                 cur.execute(query, values)
    #                 conn.commit()
    #     except Exception as e:
    #         return json.dumps({'message': 'Error updating data', 'error': str(e)})

    #     return json.dumps({'message': 'Data updated successfully'})

    # def delete(self, table, id_column):
    #     """Deletes a record from the specified table"""
    #     if table not in ["email_logs", "sellers", "buyer_agents", "products", "games"]:
    #         return json.dumps({'message': 'Invalid table name'})

    #     try:
    #         with psycopg2.connect(**self.connection_params) as conn:
    #             with conn.cursor() as cur:
    #                 query = f"DELETE FROM {table} WHERE id = %s"
    #                 cur.execute(query, (id_column,))
    #                 conn.commit()
    #     except Exception as e:
    #         return json.dumps({'message': 'Error deleting data', 'error': str(e)})

    #     return json.dumps({'message': 'Data deleted successfully'})

if __name__ == "__main__":

    # Testing
    da = DataAccess()
    # game_data = da.get_bayesian_game(game_id=1)
    # game_data = json.loads(game_data)
    # print(game_data['data'])

    data = da.update_bayesian_game(game_id=1, buyer_reservation_price= 10)
    update_data = json.loads(data)
    print(update_data)
