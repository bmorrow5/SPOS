from dash import Dash, html, dcc
import requests

app = Dash(__name__)

def get_seller_negotiation_power():
    response = requests.get('http://localhost:5000/api/get_negotiation_power')
    if response.ok:
        return response.json()
    else:
        return []

# Will edit once game logic
app.layout = html.Div([
    html.H1("Negotiation Power"),
    dcc.Dropdown(
        id='seller_np-dropdown',
        options=[{'label': seller, 'value': seller} for seller in get_seller_negotiation_power()],
        # value='Seller'  # Default value
    )
])

if __name__ == '__main__':
    app.run_server(port=8050, debug=True) 