
""" This is the main file for the application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.bayesian_fuzzy_game.product import Product
from backend.bayesian_fuzzy_game.buyer import Buyer
from backend.bayesian_fuzzy_game.seller import Seller
from backend.bayesian_fuzzy_game.negotiation_game import NegotiationGame
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProductRequest(BaseModel):
    name: str
    quantity: int
    initial_price: float
    current_price: float
    date_needed: str

class BuyerRequest(BaseModel):
    name: str
    email: str
    negotiation_power: float
    reservation_price: float
    id: str
    password: str

class SellerRequest(BaseModel):
    name: str
    email: str
    negotiation_power: float
    reservation_price: float
    product: ProductRequest

class GameRequest(BaseModel):
    buyer: BuyerRequest
    seller: SellerRequest

@app.post("/negotiate/")
def negotiate(game: GameRequest):
    try:
        # Create a new buyer
        buyer = Buyer(name = game.buyer.name, email = game.buyer.email, negotiation_power = game.buyer.negotiation_power, reservation_price = game.buyer.reservation_price, id = game.buyer.id, password = game.buyer.password)
        
        # Create a new product
        product = Product(name = game.seller.product.name, quantity = game.seller.product.quantity, initial_price = game.seller.product.initial_price, current_price = game.seller.product.current_price, date_needed = game.seller.product.date_needed)
        
        # Create a new seller
        seller = Seller(name = game.seller.name, email = game.seller.email, negotiation_power = game.seller.negotiation_power, reservation_price = game.seller.reservation_price, product = product)
        
        # Create a new game
        negotiation_game = NegotiationGame(buyer, seller)
        
        # Get the counter offer price
        counter_offer_price = negotiation_game.get_counteroffer_price()
        
        # Create a new email service
        email_service = EmailService()
        
        # Send the counter offer price to the seller
        email_service.reply_with_counteroffer([seller.email], counter_offer_price, "Counter Offer", "1")
        
        return {"counter_offer_price": counter_offer_price}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/accept/")
def accept_offer(to_email: str, message: str):
    try:
        email_service = EmailService()
        email_service.send_acceptance(to_email, message)
        return {"message": "Email sent successfully!"}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/request/")
def request_quote(product: ProductRequest, buyer_reservation_price: float):
    try:
        # Create a new product
        product = Product(name = product.name, quantity = product.quantity, initial_price = product.initial_price, current_price = product.current_price, date_needed = product.date_needed)
        
        # Create a new buyer
        buyer = Buyer(reservation_price = buyer_reservation_price)
        
        # Create a new seller
        seller = Seller(reservation_price = buyer_reservation_price, product = product)
        
        # Create a new game
        negotiation_game = NegotiationGame(buyer, seller)
        
        # Create a new email service
        email_service = EmailService()
        
        # Request a quote from the seller
        email_service.request_quote(seller, negotiation_game)
        
        return {"message": "Email sent successfully!"}
    except Exception as e:
        return {"error": str(e)}
    

@app.post("/data/")
def add_data(data: dict):
    try:
        data_service = DataService()
        data_service.add_data(data)
        return {"message": "Data added successfully!"}
    except Exception as e:
        return {"error": str(e)}
    

if __name__ == "__main__":
    
    # Get the port from the environment variable
    port = os.getenv("PORT", 8000)
    
    # Run the application
    import uvicorn
    uvicorn.run(app)
    
                
