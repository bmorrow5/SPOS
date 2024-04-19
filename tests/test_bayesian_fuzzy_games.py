import unittest
from parameterized import parameterized
from backend.bayesian_fuzzy_game.product import Product
from backend.bayesian_fuzzy_game.buyer import Buyer
from backend.bayesian_fuzzy_game.seller import Seller
from backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame

class BayesianFuzzyGamesTest(unittest.TestCase):
    """ This class will test our bayesian fuzzy games model, and will provide a check on if our bayesian fuzzy game is working
    As of the draft this is what I am currently working on. 
    """

    # Product(self, name, quantity, initial_price, current_price, date_needed)
    # Buyer(self, name, email, negotiation_power, reservation_price, id, password)
    # Seller(self, name, email, negotiation_power, reservation_price, product)



    def setUp(self):
        pass
    
    # This is reservation_price, Product(name, quantity, initial_price, current_price, date_needed), expected_counter_offer_price
    @parameterized.expand([
            (300, Product("product1", 10, 200, 150, "2024-04-30"), 100),  
            (200, Product("product2", 10, 100, 100, "2024-05-01"), 80),  
            (100, Product("product3", 10, 75, 75, "2024-05-01"), 50),  
            (50, Product("product4", 1, 50, 50, "2024-05-10"), 40),  
            (10, Product("product5", 1, 10, 10, "2024-05-10"), 8),  
    ])
    def test_get_counteroffer_price(self, reservation_price, product, expected_counter_offer_price):
        buyer = Buyer(reservation_price = reservation_price)
        seller = Seller(reservation_price = reservation_price, product = product)
        game = BayesianFuzzyGame(buyer, seller)
        counter_offer_price = game.get_counteroffer_price()
        self.assertEqual(counter_offer_price, expected_counter_offer_price)


    def test_update_game(self):
        pass
        

    def test_estimate_opponent_payoff(self):
        pass

    def test_estimate_opponent_reservation_price(self):
        pass

    def test_get_strategy(self):
        pass

    def test_simulate_negotiation(self):
        pass


if __name__ == '__main__':
    unittest.main()