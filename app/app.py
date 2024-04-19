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
from main import Main
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
buyer = data_service.read_buyer(email= user_email)
first_name = buyer['first_name']
last_name = buyer['last_name']
email_service = EmailService(email= user_email, password=user_password)

main = Main(user_email, user_password, first_name, last_name, data_service, email_service)



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
        main.request_quotes(product_name, product_quantity, product_max_price, date_needed_by, message)
        return f"Requests for quotes sent: {product_name}"
    return ""


############## Read Emails Callback ##############
@dash_app.callback(
    Output('email_container', 'children'),
    [Input('read_emails_btn', 'n_clicks')]
)
def read_emails_button(n_clicks):
    """Reads emails from the buyer's email account
       Args:
            email_list (list): Suppliers to send email to
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents
            Product (Product): Product to request quotes for
    """
    if n_clicks is None or n_clicks == 0:
        return "Press read emails to read emails"
    if n_clicks > 0:
        emails = main.email_service.read_emails()
        return f"Emails read: {emails}"
    return ""




if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8001)


