
class Player:
    
    def __init__(self, name, negotiation_power):
        self.name = name
        self.negotiation_power = negotiation_power

    def __str__(self):
        return f"{self.name} ({self.email})"
    