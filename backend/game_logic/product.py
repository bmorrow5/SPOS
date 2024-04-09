
class Product():

    def __init__(self, name, quantity, current_price, date_needed):
        self.name = name
        self.quantity = quantity
        self.current_price = current_price
        self.date_needed = date_needed
        
    def __str__(self) -> str:
        return f"Name: {self.name}, QTY: {self.quantity}, Current Price: {self.current_price}, Max Price: {self.max_price}, Date Needed: {self.date_needed}"
