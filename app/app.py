from ..backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame
from ..backend.email_service.email_service import EmailService
from ..backend.data_service.data_service import DataService
from flask import Flask, request, jsonify
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import requests
import json
import time


server = Flask(__name__)
app = Dash(__name__, server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    dcc.Input(id='product_id', type='text', placeholder='Product ID'),
    dcc.Input(id='buyer_id', type='text', placeholder='Buyer ID'),
    html.Button('Run Game', id='submit-btn', n_clicks=0),
    html.Div(id='output-container')
])

@app.callback(
    Output('output-container', 'children'),
    [Input('submit-btn', 'n_clicks')],
    [State('product_id', 'value'),
     State('buyer_id', 'value')]
)
def update_games(n_clicks, product_id, buyer_id):
    """This function will run the game when the button is clicked based on new emails
    """
    if n_clicks > 0:
        # data_service = DataService()
        # email_service = EmailService()

        # product = data_service.get_product_details(product_id)
        # buyer = data_service.get_buyer_details(buyer_id)
        # sellers = data_service.get_sellers(product_id)

        # game = BayesianFuzzyGame(product, buyer, sellers)
        # results = game.run_game()

        # for result in results:
        #     seller_email = data_service.get_seller_email(result['seller_id'])
        #     email_service.send_offer(seller_email, result)

        return f"Game run successfully for Product ID: {product_id}"
    return "Press the button to run the game."



if __name__ == '__main__':
    app.run_server(debug=True, port=8001)