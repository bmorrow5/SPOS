import skfuzzy as fuzz
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD


class GameBayesianNetwork():
    """Creates a bayesian network that measures the influence of external factors on a negotiations. 
    This will return a probability from [0,1] where 1 means no influence from outside factors,
    and 0.1 means a large negative influence fromm outside factors on a players utility. See readme for
    graphic of the network. We will use fuzzy mathematics to determine the influence of these external factors.
    """
    def __init__(self):
        self.buyer_network = None
        self.seller_network = None

    def create_buyer_network(self):
        """ This function builds the bayesian network for the buyer, and return a external factor value [0,1]
        """     
        self.buyer_network = BayesianNetwork([
            # Contractor capability, (buyer power parent node)
            ('payment_status', 'contractor_capability'),
            ('benefit_after_deal', 'contractor_capability'),
            ('offer_price', 'benefit_after_deal'),
            ('contractor_capability', 'contractor_power'),

            # Market competition, (buyer power parent node)
            ('estimated_direct_costs', 'market_competition'),
            ('number_of_suppliers', 'market_competition'),
            ('inflation', 'fluctuation_of_market_price'),
            ('Bank interest rate', 'fluctuation_of_market_price'),
            ('fluctuation_of_market_price', 'market_competition'),
            ('market_competition', 'contractor_power'),

            # Negotiaiton Deadline Pressure, (buyer power parent node)
            ('current_negotiation_time', 'negotiation_deadline_pressure'),
            ('offer_price', 'negotiation_deadline_pressure'),
            ('negotiation_deadline_pressure', 'contractor_power')
        ])
        
        




        
        # buyer_network.add_cpds()

        # Validate the model
        # assert buyer_network.check_model()

    def create_seller_network(self):
        """ This function builds the bayesian network for the seller, and returns an external factor value [0,1]
        """
        self.seller_network = BayesianNetwork([
            # Competition capability, (supplier power parent node)
            ('estimated_direct_costs', 'production_cost'),
            ('inflation', 'production_cost'),
            ('production_cost', 'competition_capability'),
            ('number_of_competitors', 'competition_capability'),
            ('overheads', 'competition_capability'),
            ('competition_capability', 'supplier_power'),

            # Negotiation deadline pressure, (supplier power parent node)
            ('overheads', 'negotiation_deadline_pressure')
            ('current_negotiation_time', 'negotiation_deadline_pressure'),
            ('offer_price', 'negotiation_deadline_pressure'),
            ('negotiation_deadline_pressure', 'supplier_power'),

            # Stability level of economy, (supplier power parent node)
            ('competition_of_market_price', 'stability_level_of_economy'),
            ('bank_interest_rate', 'stability_level_of_economy'),
            ('inflation', 'stability_level_of_economy'),
            ('stability_level_of_economy', 'supplier_power'),
        ])