import datetime
from game_classes import Product, Buyer, Seller
from bayesian_network import BayesianNetwork

class BayesianFuzzyGame():
    """ Performs the negotiation game theory, calculates utility, and returns the counteroffer price.
        The main function in this class is "update_game" which updates the game and gives counteroffer price.
        The Rubinsteins alternating offers protocol is followed with this method, and we use the Bayesian
        Fuzzy Game Model that was created by Sou-Sen Leu, Pham Vu Hong Son, and Pham Thi Hong Nhung in the paper
        Optimize Negotiation Price in Construction Procurement using Bayesian Fuzzy Game Model (2015)

        See the PDF SPOS Mathematics for more information on the model. New negotiations start with
        p=0.5, q=0.5 for the mixed strategy
    """

    def __init__(self, game_id, game_time_days, product, buyer, seller):
        new_product = Product(product['name'], 
                              product['quantity'], 
                              product['initial_price'], 
                              product['current_price'])
        new_buyer = Buyer(buyer['name'], 
                          buyer['email'], 
                          buyer['negotiation_power'], 
                          buyer['reservation_price'], 
                          buyer['deadline'], 
                          buyer['last_offer_price'])
        new_seller = Seller(seller['name'], 
                            seller['email'], 
                            seller['negotiation_power'], 
                            seller['reservation_price'], 
                            seller['deadline'], 
                            seller['last_offer_price'])
        self.game_id = game_id
        self.game_time = game_time_days
        self.product =  new_product
        self.buyer = new_buyer
        self.seller = new_seller
        

    def update_game(self):
        """Updates the game and gives counteroffer price
        """
        game = {}
        seller_offer_price = self.seller.last_offer_price

        # Check if this is a new game
        if self.buyer.last_offer_price is None:
            # Set the initial price as the counteroffer price
            self.product.initial_price = seller_offer_price

            self.get_counter_offer_price(seller_offer_price, 
                                 0, 
                                 self.buyer.deadline, 
                                 self.buyer.negotiation_power, 
                                 self.buyer.reservation_price, 
                                 self.product.initial_price, 
                                 1, 
                                 first_offer=True)
            
        # Set the sellers offer to the products current price
        self.product.current_price = seller_offer_price

        # Check if offer is acceptable            

        # Check if deadline is hit

        # Update the beliefs (bayesian networks) of buyer and seller
        # BayesianNetwork().update_beliefs(self.buyer, self.seller)
        # buyer_external_factors, seller_external_factors = BayesianNetwork().get_external_factors()
        buyer_external_factors, seller_external_factors = 1, 1

        # Define the payoff matrix
        b_Hh, b_Hl, b_Lh, b_Ll = 7.5, 0.25, 2.5, 0.75
        s_Hh, s_Hl, s_Lh, s_Ll = 7.5, 2.5, 0.25, 0.75

        # Calculate the delta and gamma values
        delta_value = self.delta(b_Hh, b_Hl, b_Lh, b_Ll)
        
        gamma_value = self.gamma()
        
        # Calculate the utilities for the buyer and seller
        buyer_utility = self.get_utility_buyer()
        seller_utility = self.get_utility_seller()

        # Now use this strategy to get counteroffer price
        counter_offer_price = self.get_counter_offer_price(seller_offer_price, 
                                                            self.game_time,
                                                            self.buyer.deadline, 
                                                            self.buyer.negotiation_power, 
                                                            self.buyer.reservation_price, 
                                                            self.product.current_price, 
                                                            1, 
                                                            first_offer=False)
        return counter_offer_price



    def update_beliefs(self):
        """Updates the beliefs of the buyer and seller
        """
        pass


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

    ## Need to check this
    def x_payoff(self, OP, IP, RP, xmin):
        """ Calculate the payoff for the given offer price. """
        return xmin + (1 - xmin) * abs(RP - OP) / abs(RP - IP)

    def adjust_strategy(history, agent):
        last_utility = history[agent]["utilities"][-1] if history[agent]["utilities"] else None
        if last_utility is not None:
            # Example adjustment: decrease lambda if utility is low to make offers more appealing
            if last_utility < 0.5:
                return 0.1  # More conservative
            else:
                return 0.9  # More aggressive
        return 0.5  # Default strategy        

    def get_counter_offer_price(previous_offer, t, tau, lambda_strategy, reservation_price, intial_price, alpha, first_offer=False):
        """
        Calculate the next offer price based on the previous offer and negotiation dynamics.
        """
        if first_offer:
            factor = (-1)**alpha * (t / tau) ** lambda_strategy
            first_offer_price = intial_price + factor * abs(reservation_price - intial_price)
            return first_offer_price
        else:
            time_factor = (t / (tau - (t - 1)))**lambda_strategy
            price_difference = abs(reservation_price - intial_price)
            adjustment = (-1)**alpha * time_factor * price_difference
            new_offer = previous_offer + adjustment
            return new_offer