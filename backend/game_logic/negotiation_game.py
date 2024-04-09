
class NegotiationGame():
    
    def __init__(self, buyer, seller):
        self.buyer = buyer
        self.seller = seller

    def delta(self, q):
        return (self.sHh - self.sHl - self.sLh + self.sLl) * q + self.sHl - self.sLl

    def gamma(self, p):
        """Gets the """
        return (self.cHh - self.cHl - self.cLh + self.cLl) * p + self.cLh - self.cLl

    def calculate_seller_utility(self, p, q):
        """Calculates the utility of the seller"""
        return self.delta(q) * self.beta * p + (self.sLh - self.sLl) * q + self.sLl

    def calculate_buyer_utility(self, p, q):
        """Calcultes the utility of the buyer """
        return self.gamma(p) * self.alpha * q + (self.cHl - self.cLl) * p + self.cLl
    
    def calculate_offer_price():
        pass


    def simulate_negotiation(self):
        round_t = 1
        tau_x = 5  # Example negotiation deadline
        lambda_x_ij = 1  # Example time-dependent strategy factor
        xmin = 0.1  # Minimum utility

        # Start negotiation rounds
        print(f"Negotiation starts for {self.product.name} between Buyer {self.buyer.name} and Seller {self.seller.name}")
        while round_t <= tau_x:
            # Simplified offer price calculation (detailed implementation may vary)
            buyer_OP = self.buyer.IP + ((-1) ** 0) * (round_t / tau_x) * lambda_x_ij * (self.buyer.RP - self.buyer.IP)
            seller_OP = self.seller.product.current_price + ((-1) ** 1) * (round_t / tau_x) * lambda_x_ij * (self.seller.product.max_price - self.seller.product.current_price)
            
            # Calculate utilities based on current strategies
            US = self.calculate_US(self.p, self.q)
            UC = self.calculate_buyer_utility(self.p, self.q)
            
            print(f"Round {round_t}: Buyer offers {buyer_OP}, Seller offers {seller_OP}")
            print(f"Utilities - Seller: {US}, Buyer: {UC}")
            
            if buyer_OP >= seller_OP:  # Agreement condition
                print(f"Agreement reached at round {round_t} with offer {seller_OP}")
                break
            
            round_t += 1

        if round_t > tau_x:
            print("Negotiation failed to reach an agreement.")