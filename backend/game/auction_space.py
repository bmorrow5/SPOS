class AuctionSpace:
    def __init__(self, name, start_price):
        self.name = name
        self.start_price = start_price
        self.bids = []

    def decide_auction_type(self):
        pass

    def add_bid(self, bid):
        self.bids.append(bid)
        return self.bids
    
    def get_bids(self):
        return self.bids
    