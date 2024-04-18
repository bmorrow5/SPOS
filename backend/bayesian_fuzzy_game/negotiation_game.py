import numpy as np


class NegotiationGame():
    """ Performs the negotiation game theory, calculates utility, and returns the counteroffer price.
    """

    def __init__(self, buyer, seller, alpha, beta, sHh, sHl, sLh, sLl, cHh, cHl, chL, cLh, cLl):
        self.buyer = buyer
        self.seller = seller
        self.alpha = alpha # Bayesian Network seller external factors
        self.beta = beta # Bayesian Network buyer external factors

        # Payoff Matrix values
        self.sHh = sHh
        self.sHl = sHl
        self.sLh = sLh
        self.sLl = sLl
        self.cHh = cHh
        self.cHl = cHl
        self.chL = chL
        self.cLh = cLh
        self.cLl = cLl

    """ See SPOS Mathematics for an explanation of the below mathematics
    """
    def delta(self, q):
        return (self.sHh - self.sHl - self.sLh + self.sLl) * q + self.sHl - self.sLl

    def gamma(self, p):
        return (self.cHh - self.cHl - self.cLh + self.cLl) * p + self.cLh - self.cLl

    def calculate_seller_utility(self, p, q):
        """Calculates the utility of the seller"""
        return self.delta(q) * self.beta * p + (self.sLh - self.sLl) * q + self.sLl

    def calculate_buyer_utility(self, p, q):
        """Calcultes the utility of the buyer """
        return self.gamma(p) * self.alpha * q + (self.cHl - self.cLl) * p + self.cLl


    def get_strategy(self):
        pass

    def estimate_opponent_payoff(self):
        pass

    def estimate_opponent_reservation_price(self):
        pass





    # This needs to be updated
    def simulate_negotiation(self):
        """Simulates negotiations using alternating offer protocol to determine strategy as published by 
        Gwak, J. and Sim, K. M. (2011). “Bayesian learning based negotiation agents for supporting negotiation with incomplete information.”
        and Leu, S.-S., Hong Son, P. V., & Hong Nhung, P. T. (2014). "Optimize negotiation price in construction procurement using Bayesian Fuzzy Game Model"
        """

        round_t = 1
        tau_x = 5  # Negotiation deadline
        lambda_x_ij = 1  # Time-dependent strategy factor
        xmin = 0.1  # Minimum utility

        # Start negotiation rounds
        print(f"Negotiation starts for {self.product.name} between Buyer {self.buyer.name} and Seller {self.seller.name}")
        while round_t <= tau_x:

            # Offer price calculation (need to update)
            buyer_OP = self.seller.product.initial_price + ((-1) ** 0) * (round_t / tau_x) * lambda_x_ij * (self.buyer.reservation_price - self.seller.product.initial_price)
            seller_OP = self.seller.product.current_price + ((-1) ** 1) * (round_t / tau_x) * lambda_x_ij * (self.seller.product.max_price - self.seller.product.current_price)
            
            # Calculate utilities based on current strategies
            seller_utility = self.calculate_seller_utility(self.p, self.q)
            buyer_utility = self.calculate_buyer_utility(self.p, self.q)
            
            print(f"Round {round_t}: Buyer offers {buyer_OP}, Seller offers {seller_OP}")
            print(f"Utilities - Seller: {seller_utility}, Buyer: {buyer_utility}")
            
            if buyer_OP >= seller_OP:  # Agreement condition
                print(f"Agreement reached at round {round_t} with offer {seller_OP}")
                break
            round_t += 1

        if round_t > tau_x:
            print("Negotiation failed to reach an agreement in time.")




    def get_counter_offer_price(self):
        """ Returns the counteroffer price after simulating negotiations and determining a strategy
        """
        # Get strategy from simulation

        # Get Utility

        # Calculate Counter Offer Price
        return 1
