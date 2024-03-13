import numpy as np
import pandas as pd
from buyer import Buyer
import seller
import negotiation_space
import auction_space
import email

class Main:
    def run_main(self):

        # Buyer logon
            # name = input("Enter your name: ")
            # id = input("Enter your employee id: ")
            # email = input("Enter your email: ")
            # password = input("Enter your password: ")

            # Test cases
            name = "John"
            id = "123"
            email = "john@company"
            password = "password"
            
            buyer = Buyer(name = name, id = id, email = email, password = password)

            print(buyer.__str__())

        # Determine negotiation or auction
            neg_or_auction = input("Enter 'neg' for negotiation or 'auction' for auction: ")
            if neg_or_auction == "neg":
                # Request bids
                email = Email(email, password)
                email.request_bids(auction_space)
                

                # Read email
                # email.read_email()

                # Negotiate
                negotiation = NegotiationSpace()
            else:
                # Auction
                # auction = Auction()
                # auction.start_auction(auction_space, buyer)
                pass
if __name__ == "__main__":
    main = Main()
    main.run_main()