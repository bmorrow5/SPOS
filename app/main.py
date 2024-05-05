import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import re
import pandas as pd
import plotly.express as px
from datetime import datetime
from backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService

class Main():

    def __init__(self, user_email, user_password):
        # Start services
        data_service = DataService()
        buyer = data_service.read_buyer(email= user_email)
        first_name = buyer['first_name']
        last_name = buyer['last_name']
        email_service = EmailService(email= user_email, password=user_password)
        
        self.user_email = user_email
        self.user_password = user_password
        self.first_name = first_name
        self.last_name = last_name
        self.data_service = data_service
        self.email_service = email_service


    ############## New Game Request Quotes ############## 
    def update_game(self, game_id, seller_counteroffer):
        old_game = self.data_service.read_game(game_id=game_id)

        game_time_days = old_game['start_date'] - datetime.now()
        game_time_days = game_time_days.days
        print("Game time days: ", game_time_days)
        product = {'name': old_game['product_name'], 
                   'quantity': old_game['product_quantity'], 
                   'initial_price': old_game['initial_price'], 
                   'current_price': old_game['current_price']}

        buyer = {'name': old_game['buyer_name'], 
                 'email': old_game['buyer_email'], 
                 'negotiation_power': old_game['buyer_negotiation_power'], 
                 'reservation_price': old_game['buyer_reservation_price'], 
                 'last_offer_price': old_game['buyer_last_offer_price'],
                 'deadline': old_game['buyer_deadline']}
        
        seller = {'name': old_game['seller_name'], 
                  'email': old_game['seller_email'], 
                  'negotiation_power': old_game['seller_negotiation_power'], 
                  'reservation_price': old_game['seller_reservation_price'], 
                  'last_offer_price': old_game['seller_last_offer_price'],
                  'deadline': old_game['seller_deadline']}


        # Update the game
        # game_time_days, product, buyer, seller, bayesian_network_variable_dict
        bayesian_game = BayesianFuzzyGame(game_time_days=game_time_days, product=product, buyer=buyer, seller=seller)
        counter_offer_price = bayesian_game.update_game()
        return counter_offer_price
        


    def seller_plot(self):
        """This will return a plot of the top sellers
        """
        # Get all sellers
        sellers = self.data_service.read_all_sellers()

        # Create a dataframe
        df = pd.DataFrame(sellers).T

        # Create a plot
        fig = px.bar(df, x=df.index, y='total_sales', title="Top Sellers", labels={'index': 'Seller ID', 'total_sales': 'Total Sales'})

        return fig

    ############## New Game Request Quotes ############## 
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
        



    ############## Read Emails, Send Counteroffers ############## 
    ############## Still working on this automation ##############
    def read_email_and_send_counteroffers(self):
        """Reads emails from the email account and sends counteroffers to the sellers
        """
        print("Reading emails")
        # Get all emails from the email account
        emails = self.email_service.read_emails(type='Unseen') # unseen or all

        # Iterate through all emails
        if emails is None:
            return "No emails to read"
        else:
            for email in emails:
                # subject = email['subject']
                # content = email['content']
                # print(subject, content)
                # Extract game_id and offer price from the email
                # game_id, offer_price = self.extract_game_id_and_price(subject=subject, content=content)
                game_id = 1
                offer_price = 60

                print(game_id, offer_price)
                # Get the game from the database
                game = self.data_service.read_game(game_id=game_id)

                # Get the product from the database
                product = self.data_service.read_product(product_id=game['product_id'])

                # Create a new BayesianFuzzyGame
                # bayesian_game = BayesianFuzzyGame(game=game, product=product)

                # Update the game
                # bayesian_game.update_game()

                # Get the counteroffer price
                # counter_offer_price = bayesian_game.counter_offer_price
                counter_offer_price = 0

                # Send the counteroffer
                # self.send_acceptance(to_email=email['sender_email'], message=f"Counteroffer: {counter_offer_price}")

                # Update the game in the database
                # self.data_service.update_game(game_id=game_id, current_price=counter_offer_price)
                message = f"Counteroffer: {counter_offer_price}"
                reply_subject = f"Re: {email['subject']}"

                self.email_service.send_emails(
                    to_emails=[email['sender_email']],
                    subject=reply_subject,
                    message=message,
                    in_reply_to=email.get('message_id'),  # Ensure to extract and pass the original Message-ID
                    references=email.get('references')  # Pass along existing references
                    )
        return "Emails read and counteroffers sent"
    

    def extract_game_id_and_price(self, subject, content):
        """This will extract the game_id and offer price from the email subject and content using regex

        Args:
            subject (string): Email subject
            content (string): Content of the email

        Returns:
            dict: game_id and offer_price
        """
        # Regex to extract game_id from the subject
        game_id_pattern = r"Request ID: \((\d+)\)"
        # Regex to extract offer_price, $123.45 or 123.45$
        price_pattern = r"\$?(\d+\.\d{2})\$?"

        game_id_match = re.search(game_id_pattern, subject)
        price_match = re.search(price_pattern, content)

        if game_id_match is not None:
            game_id = game_id_match.group(1)
        else:
            game_id = None

        if price_match is not None:
            offer_price = price_match.group(1)
        else:
            offer_price = None

        return {game_id, offer_price}





    def send_acceptance(self, to_email: str, message: str) -> str:
        """This will send an email accepting the offer

        Args:
            to_email (str): Email to send to
            message (str): Message to send
            original_message_id (str): Original message id

        Returns:
            str: Success or failure message
        """
        message = f"To Whom It May Concern,\n\nThank you for your offer we accept.\n\nThank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
        
        self.send_emails(to_emails=[to_email], subject="Acceptance", message=message)


