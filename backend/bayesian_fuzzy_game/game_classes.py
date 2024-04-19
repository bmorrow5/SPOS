
"""Classes to initialize product, buyer and seller objects
"""
class Player():
    def __init__(self, name, email, negotiation_power, reservation_price, last_offer_price):
        self.name = name
        self.email = email
        self.negotiation_power = negotiation_power
        self.reservation_price = reservation_price
        self.last_offer_price = last_offer_price    

class Buyer(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, date_product_needed, last_offer_price):
        super().__init__(name, email, negotiation_power, reservation_price, last_offer_price)
        self.date_product_needed = date_product_needed

class Seller(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, date_sale_needed, last_offer_price):
        super().__init__(name, email, negotiation_power, reservation_price, last_offer_price)
        self.date_sale_needed = date_sale_needed

class Product():
    def __init__(self, name, quantity, max_price, current_price):
        self.name = name
        self.quantity = quantity
        self.current_price = current_price