from player import Player
class Buyer(Player):
    def __init__(self, name, email, negotiation_power, id, password):
        super().__init__(name, email, negotiation_power)
        self.id = id
        self.password = password

    def __str__(self):
        return f"Name: {self.name}\nID: {self.id}\nEmail:({self.email})"