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

app.layout = dbc.Container([
    dbc.Button("Open Popup", id="open-popup", className="mb-3", n_clicks=0),
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Popup Title")),
            dbc.ModalBody("This is the content of the popup..."),
            dbc.ModalFooter(
                dbc.Button("Close", id="close-popup", className="ms-auto", n_clicks=0)
            )
        ],
        id="modal-popup",
        is_open=False  # Set to False to keep it closed on page load
    )
])



# def generate_table(dataframe, max_rows=10):
#     return html.Table([
#         html.Thead(
#             html.Tr([html.Th(col) for col in dataframe.columns])
#         ),
#         html.Tbody([
#             html.Tr([
#                 html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
#             ]) for i in range(min(len(dataframe), max_rows))
#         ])
#     ])


@app.callback(
    Output("modal-popup", "is_open"),
    [Input("open-popup", "n_clicks"), Input("close-popup", "n_clicks")],
    [State("modal-popup", "is_open")]
)
def toggle_modal(open_n, close_n, is_open):
    if open_n or close_n:
        return not is_open
    return is_open

@server.route('/')
def hello():
    return 'Hello, this is the Flask part!'

if __name__ == '__main__':
    app.run_server(debug=True, port=8001)