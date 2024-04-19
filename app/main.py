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
dash_app.title = 'SPOS - Buyer Dashboard'

# Set the session secret key for secure cookies, **** default only for development****
server.config.update(SECRET_KEY=os.getenv("SECRET_KEY", "default_secret_key")) 

# auth = dash_auth.BasicAuth(
#     dash_app,
#     auth_func= DataService.verify_user)

user = "spos6045@gmail.com"



############## New Product Request Quotes Input ############## 

new_product_form = layout.get_new_product_form()
navbar = layout.get_navbar()

dash_app.layout = html.Div(
    [navbar, new_product_form]
)


@dash_app.callback(
    Output('input_container', 'children'),
    [Input('submit_btn', 'n_clicks')],
    [State('product_name', 'value'),
     State('product_quantity', 'value'),
     State('product_max_price', 'value'),
     State('date_needed_by', 'value')]
)
def request_quotes(n_clicks, product_name, product_quantity, product_max_price, date_needed_by):
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
        # try:
        #     # Create a new product
        #     product = DataService.create_product(name=product_name, quantity=product_quantity, max_price=product_max_price, date_needed_by=date_needed_by)

        #     # Lets get a list of all sellers in the database
        #     sellers = DataService.read_all_sellers()

        #     # Get buyer from login
        #     buyer = DataService.read_buyer(first_name=, last_name=, email)
        
        #     # If message is none make a custom message for each seller
        #     if message is None:
        #         message = f"To Whom It May Concern,\n\nWe are requesting a quote for {product.quantity} {product.name}s.\n\nPlease reply to this email with your best price, and in the body of the email, not on an attachment. \n\nThank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
            
        #     # Iterate through all sellers in the database
        #     for seller in sellers:

        #         # Declare a new game
        #         game_id = DataService.create_game(seller_id = seller.seller_id, 
        #                               buyer_agent_id = buyer.buyer_agent_id, 
        #                               product_id= product.product_id, 
        #                               buyer_reservation_price= product.max_price)

        #         # We will use the game id to identify the game when replying to emails later
        #         subject = f"Request for Quote - {product.quantity} {product.name}s - Request ID: ({game_id})"
        #         EmailService.send_emails(self, [seller.email], subject, message)
        # except Exception as e:
        #      return f"Failed to send email: {e}"
        return f"Requests for quotes sent: {product_name}"
    return ""


############## New Product Form ############## 




if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8001)