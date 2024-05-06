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
    def __init__(self, variables=None):
        if variables is None:
            pass
        else: 
            self.variables = variables # A dict of all buyer and seller variables
        self.memberships = None
        self.buyer_network = None
        self.seller_network = None


    def create_buyer_network(self):
        """ This function builds the bayesian network for the buyer, and return a external factor value [0,1]
        """     
        self.buyer_network = BayesianNetwork([
            # Buyer capability, (buyer power parent node)
            ('payment_status', 'buyer_capability'),
            ('benefit_after_deal', 'buyer_capability'),
            ('offer_price', 'benefit_after_deal'),
            ('buyer_capability', 'buyer_power'),

            # Market competition, (buyer power parent node)
            ('estimated_direct_costs', 'market_competition'),
            ('number_of_suppliers', 'market_competition'),
            ('inflation', 'fluctuation_of_market_price'),
            ('bank_interest_rate', 'fluctuation_of_market_price'),
            ('fluctuation_of_market_price', 'market_competition'),
            ('market_competition', 'buyer_power'),

            # Negotiaiton Deadline Pressure, (buyer power parent node)
            ('current_negotiation_time', 'negotiation_deadline_pressure'),
            ('offer_price', 'negotiation_deadline_pressure'),
            ('negotiation_deadline_pressure', 'buyer_power')
        ])
            
        ## Get the membership functions for each variable
        #self.setup_fuzzy_memberships()

        # Normalize the membership functions
        #for node in self.buyer_network.nodes():
        #    value = self.variables.get(node, 0)  # Retrieve value or default to 0 if not found
        #    memberships = self.calculate_memberships(value, node)

            # Update CPD
        #    cpd_values = [memberships[cat] for cat in ['very_low', 'low', 'medium', 'high', 'very_high']]
        #    cpd = TabularCPD(variable=node, variable_card=5, values=[cpd_values])
        #    self.buyer_network.add_cpds(cpd)       

        # Validate the model
        #assert self.buyer_network.check_model()

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
            ('competition_capability', 'seller_power'),

            # Negotiation deadline pressure, (supplier power parent node)
            ('overheads', 'negotiation_deadline_pressure'),
            ('current_negotiation_time', 'negotiation_deadline_pressure'),
            ('offer_price', 'negotiation_deadline_pressure'),
            ('negotiation_deadline_pressure', 'seller_power'),

            # Stability level of economy, (supplier power parent node)
            ('competition_of_market_price', 'stability_level_of_economy'),
            ('bank_interest_rate', 'stability_level_of_economy'),
            ('inflation', 'stability_level_of_economy'),
            ('stability_level_of_economy', 'seller_power')
        ])

        ## Get the membership functions for each variable
        #self.setup_fuzzy_memberships()

        # Normalize the membership functions
        #for node in self.buyer_network.nodes():
        #    value = self.variables.get(node, 0)  # Retrieve value or default to 0 if not found
        #    memberships = self.calculate_memberships(value, node)
#
        #    # Update CPD
        #    cpd_values = [memberships[cat] for cat in ['very_low', 'low', 'medium', 'high', 'very_high']]
        #    cpd = TabularCPD(variable=node, variable_card=5, values=[cpd_values])
        #    self.seller_network.add_cpds(cpd)       

        # Validate the model
        #assert self.seller_network.check_model()


    def setup_fuzzy_memberships(self):
        # Set up fuzzy membership functions for each variable.
        x = np.linspace(0, 10, 100)
        self.memberships = {
        'buyer_payment_status': {
            'very_low': fuzz.trimf(x, [0, 0, 20]),
            'low': fuzz.trimf(x, [0, 20, 40]),
            'medium': fuzz.trimf(x, [20, 40, 60]),
            'high': fuzz.trimf(x, [40, 60, 80]),
            'very_high': fuzz.trimf(x, [60, 80, 100])
        },
        'buyer_capability': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'buyer_benefit_after_deal': {
            'very_low': fuzz.trimf(x, [0, 0, 20]),
            'low': fuzz.trimf(x, [0, 20, 40]),
            'medium': fuzz.trimf(x, [20, 40, 60]),
            'high': fuzz.trimf(x, [40, 60, 80]),
            'very_high': fuzz.trimf(x, [60, 80, 100])
        },
        'buyer_offer_price': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'buyer_negotiation_deadline_pressure': {
            'very_low': fuzz.trimf(x, [0, 0, 15]),
            'low': fuzz.trimf(x, [0, 15, 30]),
            'medium': fuzz.trimf(x, [15, 30, 45]),
            'high': fuzz.trimf(x, [30, 45, 60]),
            'very_high': fuzz.trimf(x, [45, 60, 60])
        },
        'buyer_current_negotiation_time': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'buyer_bank_interest_rate': {
            'very_low': fuzz.trimf(x, [0, 0, 2]),
            'low': fuzz.trimf(x, [0, 2, 4]),
            'medium': fuzz.trimf(x, [2, 4, 6]),
            'high': fuzz.trimf(x, [4, 6, 8]),
            'very_high': fuzz.trimf(x, [6, 8, 10])
        },
        'buyer_fluctuation_of_market_price': {
            'very_low': fuzz.trimf(x, [0, 0, 20]),
            'low': fuzz.trimf(x, [0, 20, 40]),
            'medium': fuzz.trimf(x, [20, 40, 60]),
            'high': fuzz.trimf(x, [40, 60, 80]),
            'very_high': fuzz.trimf(x, [60, 80, 100])
        },
        'buyer_inflation': {
            'very_low': fuzz.trimf(x, [0, 0, 2]),
            'low': fuzz.trimf(x, [0, 2, 4]),
            'medium': fuzz.trimf(x, [2, 4, 6]),
            'high': fuzz.trimf(x, [4, 6, 8]),
            'very_high': fuzz.trimf(x, [6, 8, 10])
        },
        'buyer_number_of_suppliers': {
            'very_low': fuzz.trimf(x, [0, 0, 50]),
            'low': fuzz.trimf(x, [0, 50, 100]),
            'medium': fuzz.trimf(x, [50, 100, 150]),
            'high': fuzz.trimf(x, [100, 150, 200]),
            'very_high': fuzz.trimf(x, [150, 200, 200])
        },
        'buyer_estimated_direct_costs': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'buyer_market_competition': {
            'very_low': fuzz.trimf(x, [0, 0, 20]),
            'low': fuzz.trimf(x, [0, 20, 40]),
            'medium': fuzz.trimf(x, [20, 40, 60]),
            'high': fuzz.trimf(x, [40, 60, 80]),
            'very_high': fuzz.trimf(x, [60, 80, 100])
        },
        'seller_estimated_direct_costs': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_production_cost': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_competition_capability': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_number_of_competitors': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_overheads': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_current_negotiation_time': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_offer_price': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'sell_negotiation_deadline_pressure': {
            'very_low': fuzz.trimf(x, [0, 0, 15]),
            'low': fuzz.trimf(x, [0, 15, 30]),
            'medium': fuzz.trimf(x, [15, 30, 45]),
            'high': fuzz.trimf(x, [30, 45, 60]),
            'very_high': fuzz.trimf(x, [45, 60, 60])
        },
        'seller_competition_of_market_price': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_stability_level_of_economy': {
            'very_low': fuzz.trimf(x, [0, 0, 25]),
            'low': fuzz.trimf(x, [0, 25, 50]),
            'medium': fuzz.trimf(x, [25, 50, 75]),
            'high': fuzz.trimf(x, [50, 75, 100]),
            'very_high': fuzz.trimf(x, [75, 100, 100])
        },
        'seller_bank_interest_rate': {
            'very_low': fuzz.trimf(x, [0, 0, 2]),
            'low': fuzz.trimf(x, [0, 2, 4]),
            'medium': fuzz.trimf(x, [2, 4, 6]),
            'high': fuzz.trimf(x, [4, 6, 8]),
            'very_high': fuzz.trimf(x, [6, 8, 10])
        },
        'seller_inflation': {
            'very_low': fuzz.trimf(x, [0, 0, 2]),
            'low': fuzz.trimf(x, [0, 2, 4]),
            'medium': fuzz.trimf(x, [2, 4, 6]),
            'high': fuzz.trimf(x, [4, 6, 8]),
            'very_high': fuzz.trimf(x, [6, 8, 10])
        }
    }

    def normalize_memberships(self, memberships):
        total = sum(memberships.values())
        return {k: v / total for k, v in memberships.items()}

    def calculate_memberships(self, value, variable):
        # Convert the normalized membership values to a format suitable for pgmpy CPD        
        memberships = {cat: fuzz.interp_membership(np.linspace(0, 10, 100), mf, value)
                        for cat, mf in self.memberships[variable].items()}
        return self.normalize_memberships(memberships)

    def get_external_factors():
        pass

