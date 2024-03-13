
class Seller(Player):
    def __init__(self, name, email, phone, address):
        self.email = email
        self.phone = phone
        self.address = address
        self.product = None
        self.product_price = None

    def set_product(self, product):
        self.product = product

    def set_product_price(self, product_price):
        self.product_price = product_price
    
    def __str__(self):
        return f"{self.name} ({self.email})"