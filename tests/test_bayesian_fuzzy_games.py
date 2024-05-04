import unittest
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
from parameterized import parameterized
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
            'current_price': 1000,
            }
        self.buyer_info = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'negotiation_power': 0,
            'reservation_price': 950,
            'last_offer_price': 950,
            'deadline': '2024-05-07'
        }
        self.seller_info = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'negotiation_power': 0,
            'reservation_price': 920,
            'last_offer_price': 1000,
            'deadline': '2024-10-01' # We assume they have no significant pressure to sell
        }
        self.game = BayesianFuzzyGame(game_id=1, 
                                      game_time_days=1, 
                                      product=self.product_info, 
                                      buyer=self.buyer_info, 
                                      seller=self.seller_info)
    
    def test_update_game(self):
        """Test the update_game method
        """
        self.game.update_game()

if __name__ == '__main__':
    unittest.main()