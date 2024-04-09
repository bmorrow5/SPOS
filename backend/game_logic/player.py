
class Player:
    
    def __init__(self, name, email, negotiation_power):
        self.name = name
        self.email = email
        self.negotiation_power = negotiation_power

    def __str__(self):
        return f"{self.name} ({self.email})"
    