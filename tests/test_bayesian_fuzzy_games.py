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
    def setUp(self):
        # Set up a basic game scenario
        self.product_info = {
            'name': 'Laptop',
            'quantity': 50,
            'initial_price': 10000,
            'current_price': 8750,
            }
        self.buyer_info = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'negotiation_power': 0,
            'reservation_price': 9000,
            'last_offer_price': 8000,
            'deadline': '2024-05-10'
        }
        self.seller_info = {
            'name': 'Jane Doe',
            'email': 'jane@example.com',
            'negotiation_power': 0,
            'reservation_price': None, # Unknown reservation price
            'last_offer_price': 8800,
            'deadline': None # We assume incomplete information
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