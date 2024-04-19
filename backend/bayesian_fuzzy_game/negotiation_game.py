from game_classes import Product, Buyer, Seller

class BayesianFuzzyGame():
    """ Performs the negotiation game theory, calculates utility, and returns the counteroffer price.
        The main function in this class is "update_game" which updates the game and gives counteroffer price
    """

    def __init__(self, game_id, product, buyer, seller, counter_offer_price):
        new_product = Product(product['name'], product['quantity'], product['initial_price'], product['current_price'], product['date_needed'])
        new_buyer = Buyer(buyer['name'], buyer['email'], buyer['negotiation_power'], buyer['reservation_price'], buyer['id'], buyer['password'])
        new_seller = Seller(seller['name'], seller['email'], seller['negotiation_power'], seller['reservation_price'])
        self.game_id = game_id
        self.buyer = new_buyer
        self.seller = new_seller
        self.product =  new_product
        self.current_price = product['current_price'] 
        self.counter_offer_price = counter_offer_price


    def update_game(self):
        """Updates the game and gives counteroffer price
        """
        if self.current_price is None:
            self.current_price = self.product['initial_price']
        else:
            self.current_price = self.product['current_price']

        # Get the counteroffer price
        counter_offer_price = self.get_counteroffer_price()




        pass
