import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class Main:
    def run_main(self):

        # Buyer logon
            id = input("Enter your employee id: ")
            email = input("Enter your email: ")
            password = input("Enter your password: ")
            buyer = Buyer(id = id, email = email, password = password)

        # Determine negotiation or auction
        neg_or_auction = input("Enter 'neg' for negotiation or 'auction' for auction: ")
        
        if neg_or_auction == "neg":
            # Request bids
            email = Email(email, password)
            email.request_bids(auction_space)
            
            # Read email
            email.read_email()

            # Negotiate
            negotiation = Negotiation()
            negotiation.negotiate(auction_space, buyer)
        else:
            # Auction
            auction = Auction()
            auction.start_auction(auction_space, buyer)
            

        print("Hello World")

if __name__ == "__main__":
    main = Main()
    main.run_main()