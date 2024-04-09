
class Player():
    
    def __init__(self, name, email, negotiation_power, reservation_price):
        self.name = name
        self.email = email
        self.negotiation_power = negotiation_power
        self.reservation_price = reservation_price

    def __str__(self):
        return f"{self.name} ({self.email})"
    