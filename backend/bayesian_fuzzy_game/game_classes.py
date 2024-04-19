
class Player():
    def __init__(self, name, email, negotiation_power, reservation_price, date_needed):
        self.name = name
        self.email = email
        self.negotiation_power = negotiation_power
        self.reservation_price = reservation_price
        self.date_needed = date_needed

    def __str__(self):
        return f"{self.name} ({self.email})"
    

class Buyer(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, date_needed, id, password):
        super().__init__(name, email, negotiation_power, reservation_price, date_needed)
        self.id = id
        self.password = password

    def __str__(self):
        return f"Name: {self.name}\nID: {self.id}\nEmail:({self.email})"


class Seller(Player):
    def __init__(self, name, email, negotiation_power, reservation_price, date_needed):
        super().__init__(name, email, negotiation_power, reservation_price, date_needed)

    def __str__(self):
        return f"{self.name} ({self.email})"


class Product():
    def __init__(self, name, quantity, max_price, current_price):
        self.name = name
        self.quantity = quantity
        self.max_price = max_price
        self.current_price = current_price
        
    def __str__(self) -> str:
        return f"Name: {self.name}, QTY: {self.quantity}, Current Price: {self.current_price}, Max Price: {self.max_price}, Date Needed: {self.date_needed}"
