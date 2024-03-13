
class Seller(Player):
    def __init__(self, name, id):
        self.id = id

    def __str__(self):
        return f"{self.name} ({self.email})"