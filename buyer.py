
class Seller(Player):
    def __init__(self, id, password):
        self.id = id
        self.password = password

    def __str__(self):
        return f"{self.name}"