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
        # Set up a basic game scenario
        self.product_info = {
            'name': 'Laptop',
            'quantity': 50,
            'initial_price': 1000,
            'current_price': 950,
            }
        self.buyer_info = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'negotiation_power': 7,
            'reservation_price': 900,
            'deadline': '2024-05-01',
            'last_offer_price': None
        }
        self.seller_info = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'negotiation_power': 5,
            'reservation_price': 920,
            'deadline': '2024-10-01', # We assume they have no significant pressure to sell
            'last_offer_price': None
        }
        self.game = BayesianFuzzyGame(game_id=1, product=self.product_info, buyer=self.buyer_info, seller=self.seller_info)

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