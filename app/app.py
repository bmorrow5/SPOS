import os
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


############## Start services in Main for User ##############
user_email = "spos6045@gmail.com"
user_password = "cjoisegsetxkqdxb"
main = Main(user_email, user_password)


############## Define Layout ##############
navbar = layout.get_navbar()
update_game_card = layout.get_update_game_card()
new_product_card = layout.get_launch_new_negotiation_game_card()
add_seller_card = layout.get_add_seller_card()
bayesian_network_plot = layout.get_buyer_bayesian_network()
top_sellers_plot = layout.get_seller_bayesian_network()

data = main.get_game_table_data()
df = pd.DataFrame.from_dict(data, orient='index').set_index('game_id')
game_table = layout.get_game_table(df.sort_index(ascending=True))
# read_emails_button = layout.get_read_emails_button() # Feature not yet implemented

dash_app.layout = html.Div([
    navbar,
    dbc.Row([
        # Left Column for Cards
        dbc.Col(html.Div([update_game_card, new_product_card, add_seller_card]), width=3),
        # Right Column for Plots and Table
        dbc.Col([
            dbc.Row([
                dbc.Col(html.Div([bayesian_network_plot])),
                dbc.Col(html.Div([top_sellers_plot])),
            ]),
            dbc.Row([
                dbc.Col(html.Div([game_table]))
            ])
        ], width=9)  
    ])
])

############## Update Game Callback ##############
@dash_app.callback(
    Output('input_container_1', 'children'),
    [Input('update_game_btn', 'n_clicks')],
    [State('game_id', 'value'),
     State('seller_counteroffer', 'value')]
)
def update_game_button(n_clicks, game_id, seller_counteroffer):
    """Requests quotes from all sellers in the database for a product
       Args:
            email_list (list): Suppliers to send email to
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents
            Product (Product): Product to request quotes for
    """
    if n_clicks is None or n_clicks == 0:
        return "Enter game details to update"
    if n_clicks > 0:
        counter_offer_price = main.update_game_app(game_id, seller_counteroffer)
        return f"Game Updated: {game_id}\nRecommended Counteroffer Price: {counter_offer_price:.2f}"
    return ""


############## Request Quotes Callback ##############
@dash_app.callback(
    Output('input_container_2', 'children'),
    [Input('request_quotes_btn', 'n_clicks')],
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
        return "Enter requirement details"
    if n_clicks > 0:
        print("Sending request for quotes")
        words = main.request_quotes(product_name, product_quantity, product_max_price, date_needed_by, message)
        return words
    return ""

############## Add Seller Callback ##############
@dash_app.callback(
    Output('input_container_3', 'children'),
    [Input('add_seller_btn', 'n_clicks')],
    [State('first_name', 'value'),
     State('last_name', 'value'),
     State('email', 'value')]
)
def add_seller_button(n_clicks, first_name, last_name, email):
    """Requests quotes from all sellers in the database for a product
       Args:
            email_list (list): Suppliers to send email to
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents
            Product (Product): Product to request quotes for
    """
    if n_clicks is None or n_clicks == 0:
        return "Enter seller details"
    if n_clicks > 0:
        string = main.add_seller_to_database(first_name, last_name, email)
        return string
    return ""


############## Read Emails Callback ##############
############## Feature not yet implemented ##############
#@dash_app.callback(
#    Output('email_container', 'children'),  # This will update the children of a Div with the ID 'email_status'
#    [Input('read_emails_btn', 'n_clicks')]
#)
#def read_emails_button_call(n_clicks):
#    """Reads emails from the buyer's email account
#       Args:
#            email_list (list): Suppliers to send email to
#            counter_offer_price (float): Bayesian Games counter_offer_price
#            subject (str): Email subject
#            message (str): Email contents
#            Product (Product): Product to request quotes for
#    """
#    if n_clicks is None or n_clicks == 0:
#        return "Press read emails to read emails"
#    if n_clicks > 0:
#        main.read_email_and_send_counteroffers()
#        return f"Emails read: "
#    return ""

############## Update Game Callback ##############


############## Update Graph Callback ##############





if __name__ == '__main__':
    dash_app.run_server(debug=True, port=8001)
