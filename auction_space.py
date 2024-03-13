class AuctionSpace:
    def __init__(self, name, start_price):
        self.name = name
        self.start_price = start_price
        self.bids = []