import unittest
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
from parameterized import parameterized
from app.backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame

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
        self.game = BayesianFuzzyGame(negotiation_length=50,
                                      game_time_days=1, 
                                      product=self.product_info, 
                                      buyer=self.buyer_info, 
                                      seller=self.seller_info,
                                      bayesian_network_variable_dict=None)
    
    def test_update_game(self):
        """Test the update_game method
        """
        self.game.update_game()




    # lambda_strategy, negotiation_time, total_negotiation_length, initial_price, previous_offer, reservation_price
    @parameterized.expand([
        (0.5, 10, 50, 1100, 1000, 800),  # lambda, t, tau
        (0.5, 20, 50, 1100, 1000, 800),  # lambda, t, tau
        (0.5, 30, 50, 1100, 1000, 800),  # lambda, t, tau
        (0.5, 40, 50, 1100, 1000, 800),  # lambda, t, tau
        (0.5, 49, 50, 1100, 1000, 800),  # lambda, t, tau
        (1, 10, 50, 1100, 1000, 800),  # lambda, t, tau
        (1, 20, 50, 1100, 1000, 800),  # lambda, t, tau
        (1, 30, 50, 1100, 1000, 800),  # lambda, t, tau
        (1, 40, 50, 1100, 1000, 800),  # lambda, t, tau
        (1, 49, 50, 1100, 1000, 800),  # lambda, t, tau
        (2, 10, 50, 1100, 1000, 800),  # lambda, t, tau
        (2, 20, 50, 1100, 1000, 800),  # lambda, t, tau
        (2, 30, 50, 1100, 1000, 800),  # lambda, t, tau
        (2, 40, 50, 1100, 1000, 800),  # lambda, t, tau
        (2, 49, 50, 1100, 1000, 800),  # lambda, t, tau
        (3, 10, 50, 1100, 1000, 800),  # lambda, t, tau
        (3, 20, 50, 1100, 1000, 800), 
        (3, 30, 50, 1100, 1000, 800),  # lambda, t, tau
        (3, 40, 50, 1100, 1000, 800),  # lambda, t, tau
        (3, 49, 50, 1100, 1000, 800),  # lambda, t, tau
        (4, 10, 50, 1100, 1000, 800),  # lambda, t, tau
        (4, 20, 50, 1100, 1000, 800),  # lambda, t, tau
        (4, 30, 50, 1100, 1000, 800),  # lambda, t, tau
        (4, 40, 50, 1100, 1000, 800),  # lambda, t, tau
        (4, 49, 50, 1100, 1000, 800),  # lambda, t, tau
    ])
    def test_counter_offer_variations(self, lambda_strategy, negotiation_time, total_negotiation_length, initial_price, previous_offer, reservation_price):
        result = self.game.get_counter_offer_price(
            negotiation_time=negotiation_time,
            total_negotiation_length=total_negotiation_length,
            lambda_strategy=lambda_strategy,
            reservation_price=reservation_price,
            initial_price= initial_price,
            alpha=1
            )
        print(f'Test case - Lambda: {lambda_strategy}, t: {negotiation_time}, tau: {total_negotiation_length}, Counter Offer Price: {result}')

if __name__ == '__main__':
    unittest.main()