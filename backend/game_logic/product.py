
class Product():

    def __init__(self, name, quantity, current_price, max_price, date_needed):
        self.name = name
        self.quantity = quantity
        self.current_price = current_price
        self.max_price = max_price
        self.date_needed = date_needed
        
    def __str__(self) -> str:
        print(f"Name:{self.name}, QTY: {self.quantity}, Current Price: {self.current_price}, Max Price: {self.max_price}, Date Needed: {self.date_needed}")