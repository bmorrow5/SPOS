import unittest
from parameterized import parameterized
from backend.game_logic.buyer import Buyer
from backend.game_logic.seller import Seller
from backend.game_logic.negotiation_game import NegotiationGame

class BayesianFuzzyGamesTest(unittest.TestCase):
    """ This class will test our bayesian fuzzy games model, and will provide a check on if our bayesian fuzzy game is working
    As of the draft this is what I am currently working on. 
    """

    # Buyer(self, name, email, negotiation_power, reservation_price, id, password
    # Seller(self, name, email, negotiation_power, reservation_price, product)
    @parameterized.expand([])
    def test_get_counteroffer_price(self, reservation_price, product, expected_counter_offer_price):
        buyer = Buyer(reservation_price = reservation_price)
        seller = Seller(reservation_price = reservation_price, product = product)
        game = NegotiationGame(buyer, seller)
        counter_offer_price = game.get_counteroffer_price()
        self.assertEqual(counter_offer_price, expected_counter_offer_price)



if __name__ == '__main__':
    unittest.main()