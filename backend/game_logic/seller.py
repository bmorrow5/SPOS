from player import Player

class Seller(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, product):
        super().__init__(name, email, negotiation_power, reservation_price)
        self.product = product    

    def __str__(self):
        return f"{self.name} ({self.email})"