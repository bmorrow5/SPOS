import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
from backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService
from flask import Flask, request, jsonify
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
import dash_auth
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import layout
import requests
import json
import time


server = Flask(__name__)
dash_app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
dash_app.title = "SPOS - Buyer Dashboard"

# Set the session secret key for secure cookies, **** default only for development****
server.config.update(SECRET_KEY=os.getenv("SECRET_KEY", "default_secret_key")) 

# auth = dash_auth.BasicAuth(
#     dash_app,
#     auth_func= DataService.verify_user)

## Get username and password from login
user_email = "spos6045@gmail.com"
user_password = "cjoisegsetxkqdxb"
data_service = DataService()
email_service = EmailService(email= user_email, password=user_password)
buyer = data_service.read_buyer(email= user_email)
first_name = buyer['first_name']
last_name = buyer['last_name']


## Get layout Items
new_product_form = layout.get_new_product_form()
navbar = layout.get_navbar()
read_emails_button = layout.get_read_emails_button()

## Declare layout
dash_app.layout = html.Div(
    [navbar, new_product_form, read_emails_button]
)



############## Request Quotes Callback ##############
@dash_app.callback(
    Output('input_container', 'children'),
    [Input('submit_btn', 'n_clicks')],
    [State('product_name', 'value'),
     State('product_quantity', 'value'),
     State('product_max_price', 'value'),
     State('date_needed_by', 'value')]
)
def request_quotes_button(n_clicks, product_name, product_quantity, product_max_price, date_needed_by, subject=None, message=None):
    """Requests quotes from all sellers in the database for a product
       Args:
            email_list (list): Suppliers to send email to
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents
            Product (Product): Product to request quotes for
    """
    if n_clicks is None or n_clicks == 0:
        return "Enter details and press request quotes to submit"
    if n_clicks > 0:
        try:
            # Create a new product, get sellers and current user
            product = data_service.create_product(name=product_name, quantity=product_quantity, max_price=product_max_price, date_needed_by=date_needed_by)
            sellers_dict = data_service.read_all_sellers()
            buyer_dict = data_service.read_buyer(email= user_email)

            # If message is none make a custom message for each seller
            if message is None:
                message = f"We are requesting a quote for {product['quantity']} {product['name']}.\n\nPlease reply to this email with your best price, and in the body of the email, not on an attachment."
            
            # Iterate through all sellers in the database, create a game and send an email request for quote
            for seller_id, seller_info in sellers_dict.items():
                game_id = data_service.create_game(seller_id = seller_id, 
                                      buyer_agent_id = buyer_dict['buyer_agent_id'], 
                                      product_id= product['product_id'], 
                                      buyer_reservation_price= product['max_price'])
                
                greeting = f"Hello {seller_info['first_name']} {seller_info['last_name']},"
                farewell = f"Thank you,\n\n{first_name} {last_name}\nYour Company Intl."
                message = f"{greeting}\n\n{message}\n\n{farewell}"


                subject = f"Request for Quote - {product['quantity']} {product['name']} - Request ID: ({game_id})"
                email_service.send_emails(to_emails= [seller_info['email']], subject=subject, message=message)
        except Exception as e:
             return f"Failed to send email: {e}"
        return f"Requests for quotes sent: {product_name}"
    return ""


############## Read Emails, Send Counteroffers ############## 
def read_email_and_send_counteroffers():
    """Reads emails from the email account and sends counteroffers to the sellers
    """
    # Get all emails from the email account
    emails = email_service.read_emails()
    for email in emails:
        try:
            # Get the game id from the email subject
            game_id = email['subject'].split("Request ID: (")[1].split(")")[0]
            game = data_service.read_game(game_id=game_id)
            product = data_service.read_product(product_id=game['product_id'])
            seller = data_service.read_seller(seller_id=game['seller_id'])
            buyer = data_service.read_buyer_agent(buyer_agent_id=game['buyer_agent_id'])
            game['product'] = product
            game['seller'] = seller
            game['buyer'] = buyer
            negotiation_game = BayesianFuzzyGame(product= product, buyer= buyer, seller= seller)
            counteroffer_price = negotiation_game.update_game()
            email_service.send_emails(to_emails= [seller['email']], subject=f"Counteroffer for {product['name']}", message=f"Counteroffer price: {counteroffer_price}")
        except Exception as e:
            print(f"Failed to send counteroffer: {e}")



    def update_games(self, game_id, offer_price):
        """This will update the game with the offer price

        Args:
            game_id (int): Game id
            offer_price (float): Offer price
        """
        ds = DataService()
        messages = self.read_emails()

        for message in messages:
            game_id, offer_price = self.extract_game_id_and_price(message['subject'], message.get_payload(decode=True))
            ds.update_game(game_id, offer_price)
        
        ds.update_game(game_id=game_id, offer_price)

        


    def extract_game_id_and_price(self, subject, content):
        """This will extract the game_id and offer price from the email subject and content

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






    def reply_with_counteroffer(self, to_emails: list, counter_offer_price: float, message: str, original_message_id: str) -> str:
        """This will reply with a counteroffer to the supplier with the price found by the bayesian game theory model

        Args:
            from_email (str): _description_
            to_emails (list): _description_
            counter_offer_price (float): _description_
            subject (str): _description_
            message (str): _description_

        Returns:
            str: Success or failure message
        """

        try:
            if message is None:
                message = f"Please see our counteroffer of {counter_offer_price}" 
            for email in to_emails:
                # Setup the email
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = email
                msg['In-Reply-To'] = original_message_id
                # msg['References'] = original_message_id
                msg['Subject'] = "Counter Offer"
                msg.attach(MIMEText(message, 'plain'))

                # Connect to the server and send the email
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                try:
                    server.login(self.email, self.password)
                except Exception as e:
                    print(f"Failed to login: {e}")
                text = msg.as_string()
                server.sendmail(self.email, email, text)
                server.quit()
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


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




if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8001)


