import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
from backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService


class Main():

    def __init__(self, user_email, user_password, first_name, last_name, data_service, email_service):
        self.user_email = user_email
        self.user_password = user_password
        self.first_name = first_name
        self.last_name = last_name
        self.data_service = data_service
        self.email_service = email_service


    def request_quotes(self, product_name, product_quantity, product_max_price, date_needed_by, message=None):
        try:
            
            # Create a new product, get sellers and current user
            product = self.data_service.create_product(name=product_name, quantity=product_quantity, max_price=product_max_price, date_needed_by=date_needed_by)
            sellers_dict = self.data_service.read_all_sellers()
            buyer_dict = self.data_service.read_buyer(email= self.user_email)

            # If message is none make a custom message for each seller
            if message is None:
                message = f"We are requesting a quote for {product['quantity']} {product['name']}.\n\nPlease reply to this email with your best price, and in the body of the email, not on an attachment."
            
            # Iterate through all sellers in the database, create a game and send an email request for quote
            for seller_id, seller_info in sellers_dict.items():
                game_id = self.data_service.create_game(seller_id = seller_id, 
                                      buyer_agent_id = buyer_dict['buyer_agent_id'], 
                                      product_id= product['product_id'], 
                                      buyer_reservation_price= product['max_price'])
                
                greeting = f"Hello {seller_info['first_name']} {seller_info['last_name']},"
                farewell = f"Thank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
                message = f"{greeting}\n\n{message}\n\n{farewell}"


                subject = f"Request for Quote - {product['quantity']} {product['name']} - Request ID: ({game_id})"
                self.email_service.send_emails(to_emails= [seller_info['email']], subject=subject, message=message)
        except Exception as e:
             return f"Failed to send email: {e}"