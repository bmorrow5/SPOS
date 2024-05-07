import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html, dash_table
import dash_cytoscape as cyto


"""This file contains all the design components. This callbacks to the backend are done in app.py
The layout is then rendered in the app.py file.
"""
def get_navbar():
    """This is the top of the page navbar
    """
    dashboard = dbc.Navbar(
        dbc.Container(
        [
            dbc.Col(dbc.NavbarBrand("Strategic Procurement Optimization System (SPOS)", href="#"), sm=3, md=2),
            # dbc.Col(dbc.Input(type="search", placeholder="Search here")),
            dbc.Col(
                dbc.Nav(
                    dbc.Container(dbc.NavItem(dbc.NavLink("Sign out"))),
                    navbar=True,
                ),
                width="auto",
            ),
        ], 
        fluid=True
    ),
    color="dark",
    dark=True,
    )
    return dashboard


def get_update_game_card():
    """This is the form for updating the game with new seller counteroffers
    """
    update_game_form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='input_container_1'),                ),
            ],
            className="mb-3",
            justify= "start"
        ),
        dbc.Row(
            [
                # Product Name
                dbc.Label("Game ID", html_for="game_id", width=4, md=5, sm=2),
                dbc.Col(
                    dbc.Input(type="number", id="game_id", placeholder="Game ID"),
                    width="auto"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Label("Total Seller Counteroffer Price (USD)", html_for="seller_counteroffer", width=4, md=5, sm=2),
                dbc.Col(
                    dbc.Input(type="number", id="seller_counteroffer", placeholder="(Quantity*PPU)"),
                    width="auto"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Update Game", color="primary", id='update_game_btn'),
                    width={"size": "auto", "offset": "auto"}
                ),
            ],
            className="mb-3",
            justify= "end"
        ),
    ],
    className="g-2 align-items-end" # g-2 is the gap between the columns
    )
    card = dbc.Card(
        [
            dbc.CardHeader("Update Game"),
            dbc.CardBody(update_game_form),
        ],
        style={'marginTop': '20px', 'marginBottom': '20px', 'marginLeft': '20px'} # Add margins for better spacing if needed
    )
    return card

def get_launch_new_negotiation_game_card():
    """This is the horozontal input form for requesting quotes for a new product
    """
    new_product_form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='input_container_2')                ),
            ],
            className="mb-3",
            justify= "start"
        ),
        dbc.Row(
            [
                # Product Name
                dbc.Label("Product Name", html_for="product_name", width=4, md=4, sm=2),
                dbc.Col(
                    dbc.Input(type="text", id="product_name", placeholder="Product Name"),
                    width="auto"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Quantity Needed
                dbc.Label("Quantity Needed", html_for="product_quantity", width=4, md=4, sm=2),
                dbc.Col(
                    dbc.Input(type="number", id="product_quantity", placeholder="Quantity Needed"),
                    width="auto"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Max Price per Unit
                dbc.Label("Max Price per Unit (USD)", html_for="product_max_price", width=4, md=4, sm=2),
                dbc.Col(
                    dbc.Input(type="number", id="product_max_price", placeholder="Max Price per Unit (USD)"),
                    width="auto"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row([
                # Date Needed By
                dbc.Label("Date Needed By", html_for="date_needed_by", width=4, md=4, sm=2),
                dbc.Col(
                    dbc.Input(type="dateString", id="date_needed_by", placeholder="YYYY-MM-DD"),
                    width="auto"
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Request Quotes", color="primary", id='request_quotes_btn'),
                    width={"size": "auto", "offset": 2}
                ),
            ],
            className="mb-3",
            justify= "end"

        ),
    ],
    className="g-2 align-items-end" # g-2 is the gap between the columns
    )
    # Wrapping the form inside a Card
    card = dbc.Card(
        [
            dbc.CardHeader("Launch New Negotiation Game"),
            dbc.CardBody(new_product_form),
        ],
        style={'marginTop': '20px', 'marginBottom': '20px', 'marginLeft': '20px'} # Add margins for better spacing if needed
    )
    return card


def get_add_seller_card():
    add_seller_form = dbc.Form(
            [   
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='input_container_3'),
                ),
            ],
            className="mb-3",
            justify= "start"
        ),
        dbc.Row(
        [
            # Quantity Needed
            dbc.Label("First Name", html_for="first_name", width=4, md=4, sm=2),
            dbc.Col(
                dbc.Input(type="text", id="first_name", placeholder="First Name"),
                width="auto"
            ),
        ],
        className="mb-3",
    ),
    dbc.Row(
        [
            # Max Price per Unit
            dbc.Label("Last Name", html_for="last_name", width=4, md=4, sm=2),
            dbc.Col(
                dbc.Input(type="text", id="last_name", placeholder="Last Name"),
                width="auto"
            ),
        ],
        className="mb-3",
    ),
    dbc.Row([
            # Date Needed By
            dbc.Label("Email", html_for="email", width=4, md=4, sm=2),
            dbc.Col(
                dbc.Input(type="text", id="email", placeholder="Email"),
                width="auto"
            ),
        ],
        className="mb-3",
    ),
    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Add Seller", color="primary", id='add_seller_btn'),
                width={"size": "auto", "offset": 2},
            ),
        ],
        className="ml-auto",
        justify= "end"

    ),
    ],
    className="g-2 align-items-end" # g-2 is the gap between the columns
    )
    # Wrapping the form inside a Card
    card = dbc.Card(
    [
        dbc.CardHeader("Add Seller to Database"),
        dbc.CardBody(add_seller_form),
    ],
    style={'marginTop': '20px', 'marginBottom': '20px', 'marginLeft': '20px'} # Add margins for better spacing if needed
    )
    return card


def get_buyer_bayesian_network(elements):
    """This is the plot for the Bayesian Network
    """
    bayesian_network_plot = dbc.Card(
        [
            dbc.CardHeader("Buyer Bayesian Network (Interactive)"),
            dbc.CardBody([
                html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-1',
            elements=elements,
            style={'width': '100%', 'height': '350px'},
            layout={
                'name': 'breadthfirst',
                'roots': '#buyer_power'})
                        ])
                        ]),
        ],
        style={'marginTop': '20px', 'marginBottom': '20px', 'marginRight': '20px'} # Add margins for better spacing if needed
    )
    return bayesian_network_plot


def get_seller_bayesian_network(elements):
    """This is the plot for the top sellers
    """
    bayesian_network_plot = dbc.Card(
        [
            dbc.CardHeader("Seller Bayesian Network (Interactive)"),
            dbc.CardBody([
                html.Div([
        cyto.Cytoscape(
            id='cytoscape-layout-2',
            elements=elements,
            style={'width': '100%', 'height': '350px'},
            layout={
                'name': 'breadthfirst',
                'roots': '#seller_power'})
                        ])
                        ]),
        ],
        style={'marginTop': '20px', 'marginBottom': '20px', 'marginRight': '20px'} # Add margins for better spacing if needed
    )
    return bayesian_network_plot


def get_game_table(data):
    """This is the table for the game
    """
    game_table = dbc.Table.from_dataframe(
    data, striped=True, bordered=True, hover=True, index=True, responsive=True
    )
    
    padded_table = html.Div(game_table, style={'padding': '20px'})
    return padded_table


#def get_read_emails_button():
#    """ NOT YET IMPLEMENTED
#    This is the button that triggers the reading of emails and updating of the game
#    """
#
#    button_form = dbc.Form(
#        [
#            dbc.Row(
#                [
#                    dbc.Col(
#                        dbc.Button("Read Emails and Send Counteroffers", color="primary", id='read_emails_btn'),
#                        width={"size": 6, "offset": 1}
#                    ),
#                ],
#                className="mb-3",
#            ),
#            dbc.Row(
#            [
#                dbc.Col(
#                    html.Div(id='email_container'),
#                    width={"size": 6, "offset": 1}
#                ),
#            ],
#            className="mb-3",
#        ),
#        ]
#    )
#    return button_form