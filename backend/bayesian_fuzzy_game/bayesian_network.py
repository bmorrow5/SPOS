import numpy as np
import skfuzzy as fuzz
from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD


class GameBayesianNetwork():
    """Creates a bayesian network that measures the influence of external factors on a negotiations. 
    This will return a probability from [0,1] where 1 means no influence from outside factors,
    and 0.1 means a large negative influence fromm outside factors on a players utility. See readme for
    graphic of the network. We will use fuzzy mathematics to determine the influence of these external factors.
    """
    def __init__(self, 
                 buyer_payment_status, 
                 buyer_capability, 
                 buyer_benefit_after_deal, 
                 buyer_offer_price, 
                 buyer_negotiation_deadline_pressure, 
                 buyer_current_negotiation_time, 
                 buyer_bank_interest_rate,
                 buyer_fluctuation_of_market_price,
                 buyer_inflation,
                 buyer_number_of_suppliers,
                 buyer_estimated_direct_costs,
                 buyer_market_competition,
                 seller_estimated_direct_costs,
                 seller_production_cost,
                 seller_competition_capability,
                 seller_number_of_competitors,
                 seller_overheads,
                 seller_current_negotiation_time,
                 seller_offer_price,
                 sell_negotiation_deadline_pressure,
                 seller_competition_of_market_price,
                 seller_stability_level_of_economy,
                 seller_bank_interest_rate,
                 seller_inflation
                 ):
        self.buyer_network = None
        self.seller_network = None

        self.buyer_payment_status = buyer_payment_status
        self.buyer_capability = buyer_capability
        self.buyer_benefit_after_deal = buyer_benefit_after_deal
        self.buyer_offer_price = buyer_offer_price
        self.buyer_negotiation_deadline_pressure = buyer_negotiation_deadline_pressure
        self.buyer_current_negotiation_time = buyer_current_negotiation_time
        self.buyer_bank_interest_rate = buyer_bank_interest_rate
        self.buyer_fluctuation_of_market_price = buyer_fluctuation_of_market_price
        self.buyer_inflation = buyer_inflation
        self.buyer_number_of_suppliers = buyer_number_of_suppliers
        self.buyer_estimated_direct_costs = buyer_estimated_direct_costs
        self.buyer_market_competition = buyer_market_competition

        self.seller_estimated_direct_costs = seller_estimated_direct_costs
        self.seller_production_cost = seller_production_cost
        self.seller_competition_capability = seller_competition_capability
        self.seller_number_of_competitors = seller_number_of_competitors
        self.seller_overheads = seller_overheads
        self.seller_current_negotiation_time = seller_current_negotiation_time
        self.seller_offer_price = seller_offer_price
        self.sell_negotiation_deadline_pressure = sell_negotiation_deadline_pressure
        self.seller_competition_of_market_price = seller_competition_of_market_price
        self.seller_stability_level_of_economy = seller_stability_level_of_economy
        self.seller_bank_interest_rate = seller_bank_interest_rate
        self.seller_inflation = seller_inflation


    def create_buyer_network(self):
        """ This function builds the bayesian network for the buyer, and return a external factor value [0,1]
        """     
        self.buyer_network = BayesianNetwork([
            # Buyer capability, (buyer power parent node)
            ('payment_status', 'buyer_capability'),
            ('benefit_after_deal', 'buyer_capability'),
            ('offer_price', 'benefit_after_deal'),
            ('buyer_capability', 'contractor_power'),

            # Market competition, (buyer power parent node)
            ('estimated_direct_costs', 'market_competition'),
            ('number_of_suppliers', 'market_competition'),
            ('inflation', 'fluctuation_of_market_price'),
            ('bank_interest_rate', 'fluctuation_of_market_price'),
            ('fluctuation_of_market_price', 'market_competition'),
            ('market_competition', 'contractor_power'),

            # Negotiaiton Deadline Pressure, (buyer power parent node)
            ('current_negotiation_time', 'negotiation_deadline_pressure'),
            ('offer_price', 'negotiation_deadline_pressure'),
            ('negotiation_deadline_pressure', 'contractor_power')
        ])
        
    
        
        # self.buyer_network.add_cpds()

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
            ('stability_level_of_economy', 'supplier_power')
        ])


        def setup_fuzzy_membership(self):
            # Set up fuzzy membership functions for each variable.
            # Example for one variable - you will need to define the ranges and shapes based on your domain knowledge.
            x = np.linspace(0, 10, 100)
            self.memberships = {
                'offer_price': {
                    'very_low': fuzz.trimf(x, [0, 2, ]),
                    'low': fuzz.trimf(x, [2, 4, ]),
                    'medium': fuzz.trimf(x, [4, 6, ]),
                    'high': fuzz.trimf(x, [6, 8, ]),
                    'very_high': fuzz.trimf(x, [8, 10, ])
                }
                # Add other variables similarly
            }

        def normalize_memberships(self, memberships):
            total = sum(memberships.values())
            return {k: v / total for k, v in memberships.items()}

        def calculate_memberships(self, value, variable):
            # Convert the normalized membership values to a format suitable for pgmpy CPD
            variables = [self.buyer_payment_status, self.buyer_capability, self.buyer_benefit_after_deal, self.buyer_offer_price, 
                 self.buyer_negotiation_deadline_pressure, self.buyer_current_negotiation_time, self.buyer_bank_interest_rate,
                 self.buyer_fluctuation_of_market_price, self.buyer_inflation, self.buyer_number_of_suppliers, self.buyer_estimated_direct_costs,
                 self.buyer_market_competition, self.seller_estimated_direct_costs, self.seller_production_cost, self.seller_competition_capability,
                 self.seller_number_of_competitors, self.seller_overheads, self.seller_current_negotiation_time, self.seller_offer_price, 
                 self.sell_negotiation_deadline_pressure, self.seller_competition_of_market_price, self.seller_stability_level_of_economy,
                 self.seller_bank_interest_rate, self.seller_inflation]
            memberships = {cat: fuzz.interp_membership(np.linspace(0, 10, 100), mf, value)
                           for cat, mf in self.memberships[variable].items()}
            return self.normalize_memberships(memberships)

        def update_cpd(self, node, probabilities):
            cpd_values = [probabilities[cat] for cat in ['very_low', 'low', 'medium', 'high', 'very_high']]
            cpd = TabularCPD(variable=node, variable_card=5, values=[cpd_values])
            self.network.add_cpds(cpd)
            assert self.network.check_model()  # Validate the model

        def calculate_cpd_values(self):
            pass

        def get_external_factors():
            pass


