import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, current_dir)
from datetime import datetime
from game_classes import Product, Buyer, Seller
from bayesian_network import GameBayesianNetwork

class BayesianFuzzyGame():
    """ Performs the negotiation game theory, calculates utility, and returns the counteroffer price.
        The main function in this class is "update_game" which updates the game and gives counteroffer price.
        The Rubinsteins alternating offers protocol is followed with this method, and we use the Bayesian
        Fuzzy Game Model that was created by Sou-Sen Leu, Pham Vu Hong Son, and Pham Thi Hong Nhung in the paper
        Optimize Negotiation Price in Construction Procurement using Bayesian Fuzzy Game Model (2015)

        See the PDF SPOS Mathematics for more information on the model. New negotiations start with
        p=0.5, q=0.5 for the mixed strategy
    """

    def __init__(self, negotiation_length, game_time_days, product, buyer, seller, bayesian_network_variable_dict):
        new_product = Product(product['name'], 
                              product['quantity'], 
                              product['initial_price'], 
                              product['current_price'])
        new_buyer = Buyer(buyer['name'], 
                          buyer['email'], 
                          buyer['negotiation_power'], 
                          buyer['reservation_price'], 
                          buyer['last_offer_price'],
                          buyer['deadline'])
        new_seller = Seller(seller['name'], 
                            seller['email'], 
                            seller['negotiation_power'], 
                            seller['reservation_price'], 
                            seller['last_offer_price'],
                            seller['deadline'])
        self.negotiation_length = negotiation_length
        self.game_time = game_time_days
        self.product =  new_product
        self.buyer = new_buyer
        self.seller = new_seller
        self.bayesian_network_variable_dict = bayesian_network_variable_dict
        

    def update_game(self):
        """Updates the game and gives counteroffer price
        """
        game = {}
        seller_offer_price = self.seller.last_offer_price

        first_offer = False

        # Check if this is a new game
        if self.buyer.last_offer_price is None:
            # Set the initial price as the counteroffer price
            self.product.initial_price = seller_offer_price
            first_offer = True
            
        # Set the sellers offer to the products current price
        self.product.current_price = seller_offer_price

        # Update the beliefs (bayesian networks) of buyer and seller
        # BayesianNetwork().update_beliefs(self.buyer, self.seller)
        # buyer_external_factors, seller_external_factors = BayesianNetwork().get_external_factors()
        buyer_external_factor_prob, seller_external_factor_prob = 1, 1

        # Define the payoff matrix
        b_Hh, b_Hl, b_Lh, b_Ll = 7.5, 0.25, 2.5, 0.75
        s_Hh, s_Hl, s_Lh, s_Ll = 7.5, 2.5, 0.25, 0.75

        # Mixed strategy probabilities, these will be adjusted by our external factors from our bayesian network.
        # We start with a mixed strategy of 0.5 for both buyer and seller
        p = 0.5
        q = 0.5

        # Calculate the delta and gamma values for our utilities
        gamma_value = self.gamma(q, b_Hh, b_Hl, b_Lh, b_Ll)
        delta_value = self.delta(p, s_Hh, s_Hl, s_Lh, s_Ll)
        
        # Get the best strategy for the buyer and seller.  
        # Utility is lambda in math doc, it is the strategy, a value between 1 and 10 depending on the specific strategy
        buyer_utility = self.get_utility_buyer(buyer_external_factor_prob, p, q, b_Hl, b_Ll, gamma_value)
        seller_utility = self.get_utility_seller(seller_external_factor_prob, p, q, s_Hl, s_Ll, delta_value)
        # print("Buyer utility: ", buyer_utility)
        # print("Seller utility: ", seller_utility)

        # Now use this strategy to get counteroffer price
        counter_offer_price = self.get_counter_offer_price(previous_offer = seller_offer_price, 
                                                           t  = self.game_time, 
                                                           tau = self.negotiation_length, 
                                                           lambda_strategy = seller_utility, # Basing our offer off opponent predicted utility 
                                                           reservation_price = self.buyer.reservation_price, 
                                                           intial_price = self.product.initial_price, 
                                                           alpha = 1,  # 1 for supplier and 0 for buyer
                                                           first_offer=first_offer # Modifies counteroffer price if first offer
                                                           )
        # print(counter_offer_price)
        # Check if current offer is acceptable U_s(OP_c^t) > U_s(OP_s^t-1)
        # Need to return a json with the bayesian network and the counter offer price
        game['bayesian_network'] = self.bayesian_network_variable_dict
        game['counter_offer_price'] = counter_offer_price
        game['buyer_utility'] = buyer_utility
        game['seller_utility'] = seller_utility
        return game


    """ Delta and gamma are the coefficients of p in the utility functions of the buyer and seller.
    """
    def delta(self, buyer_prob, s_Hh, s_Hl, s_Lh, s_Ll):
        """Calculates delta, the sign of the coeffient of p for the seller's utility function.
        q is the buyer's mixed strategy probability of choosing the high strategy.
        """ 
        return (s_Hh - s_Hl - s_Lh + s_Ll) * buyer_prob + s_Hl - s_Ll

    def gamma(self, supplier_prob, b_Hh, b_Hl, b_Lh, b_Ll):
        """Calculates gamma, the sign of the coeffient of p for the seller's utility function.
        p is the supplier's mixed strategy probability of choosing the high strategy.
        """
        return (b_Hh - b_Hl - b_Lh + b_Ll) * supplier_prob + b_Lh - b_Ll

    def get_utility_buyer(self, external_factor_prob, supplier_prob, buyer_prob, b_Hl, b_Ll, gamma_value):
        """ Calculate buyer's utility with consideration of external factors
        """
        return gamma_value * external_factor_prob * buyer_prob + (b_Hl - b_Ll) * supplier_prob + b_Ll

    def get_utility_seller(self, external_factor_prob, supplier_prob, buyer_prob, s_Lh, s_Ll, delta_value):
        """ Calculate seller's utility with consideration of external factors. """
        return delta_value * external_factor_prob * supplier_prob + (s_Lh - s_Ll) * buyer_prob + s_Ll

    ## This is not used in our model
    def x_payoff(self, OP, IP, RP, xmin):
        """ Calculate the payoff for the given offer price. """
        return xmin + (1 - xmin) * abs(RP - OP) / abs(RP - IP)

    def get_counter_offer_price(self, previous_offer, t, tau, lambda_strategy, reservation_price, intial_price, alpha, first_offer=False):
        """
        Calculate the next offer price based on the previous offer and negotiation dynamics.
        """
        if first_offer:
            factor = (-1)**alpha * (t / tau) ** lambda_strategy
            first_offer_price = intial_price + factor * abs(reservation_price - intial_price)
            return first_offer_price
        else:
            time_factor = (t / (tau - (t - 1))) ** lambda_strategy
            price_difference = abs(reservation_price - previous_offer)
            adjustment = (-1)**alpha * time_factor * price_difference
            new_offer = previous_offer + adjustment
            return new_offer