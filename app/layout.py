import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash import Dash, dcc, html



def get_new_product_form():
    """This is the form for requesting quotes for a new product
    """
    new_product_form = dbc.Form(
    [
        dbc.Row(
            [
                dbc.Col(
                    html.Div(id='input_container'),
                    width={"size": 6, "offset": 1}
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Product Name
                dbc.Label("Product Name", html_for="product_name", width=2),
                dbc.Col(
                    dbc.Input(type="text", id="product_name", placeholder="Product Name"),
                    width=2
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Quantity Needed
                dbc.Label("Quantity Needed", html_for="product_quantity", width=2),
                dbc.Col(
                    dbc.Input(type="number", id="product_quantity", placeholder="Quantity Needed"),
                    width=2
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                # Max Price per Unit
                dbc.Label("Max Price per Unit (USD)", html_for="product_max_price", width=2),
                dbc.Col(
                    dbc.Input(type="number", id="product_max_price", placeholder="Max Price per Unit (USD)"),
                    width=2
                ),
            ],
            className="mb-3",
        ),
        dbc.Row([
                # Date Needed By
                dbc.Label("Date Needed By", html_for="date_needed_by", width=2),
                dbc.Col(
                    dbc.Input(type="dateString", id="date_needed_by", placeholder="YYYY-MM-DD"),
                    width=2
                ),
            ],
            className="mb-3",
        ),
        dbc.Row(
            [
                dbc.Col(
                    dbc.Button("Request Quotes", color="primary", id='submit_btn'),
                    width={"size": 2, "offset": 2}
                ),
            ],
            className="mb-3",
        ),
    ],
    className="g-2 align-items-end" # g-2 is the gap between the columns
    )
    return new_product_form


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
    ),
    color="dark",
    dark=True,
    )
    return dashboard


def get_read_emails_button():
    """This is the button that triggers the reading of emails
    """
    read_emails_button = dbc.Button("Read Emails and Send Counteroffers", color="primary", id='read_emails_btn')
    return read_emails_button