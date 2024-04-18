from backend.bayesian_fuzzy_game.negotiation_game import BayesianFuzzyGame
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService


class Main():


    def __init__(self):
        self.data_service = DataService()
        self.email_service = EmailService()


    # def update_game(self, game_id):
    #     product = self.data_service.get_product_details(product_id)
    #     buyer = self.data_service.get_buyer_details(buyer_id)
    #     sellers = self.data_service.get_sellers(product['product_id'])

    #     game = BayesianFuzzyGame(product, buyer, sellers)
    #     negotiation_results = game.run_game()

    #     for result in negotiation_results:
    #         seller_info = next((s for s in sellers if s['seller_id'] == result['seller_id']), None)
    #         if seller_info:
    #             self.email_service.send_offer(seller_info['email'], result)



def main():
    data_service = DataService()
    email_service = EmailService()

    product = data_service.get_product_details(product_id=1)
    buyer = data_service.get_buyer_details(buyer_id=1)
    sellers = data_service.get_sellers(product['product_id'])

    game = BayesianFuzzyGame(product, buyer, sellers)
    negotiation_results = game.run_game()

    for result in negotiation_results:
        seller_info = next((s for s in sellers if s['seller_id'] == result['seller_id']), None)
        if seller_info:
            email_service.send_offer(seller_info['email'], result)


if __name__ == "__main__":
    main()
