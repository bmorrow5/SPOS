from game_classes import Product, Buyer, Seller
import nashpy as nash

class BayesianFuzzyGame():
    """ Performs the negotiation game theory, calculates utility, and returns the counteroffer price.
        The main function in this class is "update_game" which updates the game and gives counteroffer price.
        The Rubinsteins alternating offers protocol is followed with this method, and we use the Bayesian
        Fuzzy Game Model that was created by Sou-Sen Leu, Pham Vu Hong Son, and Pham Thi Hong Nhung in the paper
        Optimize Negotiation Price in Construction Procurement using Bayesian Fuzzy Game Model (2015)

        See the PDF SPOS Mathematics for more information on the model. New negotiations start with
        p=0.5, q=0.5 for the mixed strategy
    """

    def __init__(self, game_id, product, buyer, seller):
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

        # Check if the new offer is acceptable

        # If not acceptable get the counteroffer price
        counter_offer_price = self.get_counter_offer_price(seller_offer_price, 
                                 0, 
                                 self.buyer.deadline, 
                                 self.buyer.negotiation_power, 
                                 self.buyer.reservation_price, 
                                 self.product.current_price, 
                                 1, 
                                 first_offer=False)

        return counter_offer_price


    def delta(q, s_Hh, s_Hl, s_Lh, s_Ll):
        """Calculates delta, the sign of the coeffient of p for the seller's utility function.
        """ 
        return (s_Hh - s_Hl - s_Lh + s_Ll) * q + s_Hl - s_Ll

    def gamma(p, b_Hh, b_Hl, b_Lh, b_Ll):
        """Calculates gamma, the sign of the coeffient of p for the seller's utility function.
        """
        return (b_Hh - b_Hl - b_Lh + b_Ll) * p + b_Lh - b_Ll

    def utility_buyer(p, q, b_Hl, b_Ll, gamma_value):
        """ Calculate buyer's utility with consideration of external factors
        """
        # alpha = BayesianNetwork().get_alpha() # Get external factor influence
        alpha = 1 
        return gamma_value * alpha * q + (b_Hl - b_Ll) * p + b_Ll

    def utility_supplier(p, q, s_Lh, s_Ll, delta_value):
        """ Calculate supplier's utility with consideration of external factors. """
        # beta = BayesianNetwork().get_beta() # Get external factor influence
        beta = 1
        return delta_value * beta * p + (s_Lh - s_Ll) * q + s_Ll

    ## Need to check this
    def x_payoff(OP, IP, RP, xmin):
        """ Calculate the utility for the given offer price. """
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

    def get_counter_offer_price(previous_offer, t, tau, lambda_ij, RP, IP, alpha, first_offer=False):
        """
        Calculate the next offer price based on the previous offer and negotiation dynamics.
        """
        if first_offer:
            factor = (-1)**alpha * (t / tau) ** lambda_ij
            return IP + factor * abs(RP - IP)
        else:
            time_factor = (t / (tau - (t - 1)))**lambda_ij
            price_difference = abs(RP - IP)
            adjustment = (-1)**alpha * time_factor * price_difference
            new_offer = previous_offer + adjustment
            return new_offer
        