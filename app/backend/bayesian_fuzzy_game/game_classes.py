
"""Classes to initialize product, buyer and seller objects
"""
class Player():
    def __init__(self, name, email, negotiation_power, reservation_price, last_offer_price, deadline):
        self.name = name
        self.email = email
        self.negotiation_power = negotiation_power
        self.reservation_price = reservation_price
        self.last_offer_price = last_offer_price    
        self.deadline = deadline

class Buyer(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, last_offer_price, deadline):
        super().__init__(name, email, negotiation_power, reservation_price, last_offer_price, deadline)

class Seller(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, last_offer_price, deadline):
        super().__init__(name, email, negotiation_power, reservation_price, last_offer_price, deadline)

class Product():
    def __init__(self, name, quantity, initial_price, current_price):
        self.name = name
        self.quantity = quantity
        self.initial_price = initial_price
        self.current_price = current_price