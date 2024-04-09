from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD


class GameBayesianNetwork():
    """Creates a bayesian network that measures the influence of external factors on a negotiations. 
    This will return a probability from [0,1] where 1 means no influence from outside factors,
    and 0.1 means a large negative influence fromm outside factors on a players utility. 
    """
    def __init__(self):
        None

    def create_buyer_network():
        """ This function builds the bayesian network for the buyer, and return a external factor value [0,1]
        """     
        model = BayesianNetwork([
            ('Payment status', 'Contractor capability'),
            ('Contractor capability', 'Contractor power'),
            ('Benefit after deal', 'Contractor power'),
            ('Offer price', 'Contractor power'),
            ('Estimated direct cost', 'Contractor power'),
            ('Market competition', 'Contractor power'),
            ('Market competition', 'Fluctuation of market price'),
            ('No of suppliers', 'Market competition'),
            ('Inflation', 'Market competition'),
            ('Inflation', 'Bank interest rate'),
            ('Current negotiation time', 'Negotiation deadline pressure'),
            ('Bank interest rate', 'Negotiation deadline pressure'),
            ('Negotiation deadline pressure', 'Contractor power'),
            ('Estimated direct cost', 'Supplier power'),
            ('Production cost', 'Supplier power'),
            ('Competition capability', 'Supplier power'),
            ('No of competitors', 'Competition capability'),
            ('Overheads', 'Supplier power'),
            ('Current negotiation time', 'Supplier power'),
            ('Offer price', 'Supplier power'),
            ('Stability level of economic', 'Supplier power'),
            ('Competition of market price', 'Supplier power'),
            ('Negotiation deadline pressure', 'Supplier power'),
            ('Bank interest rate', 'Competition of market price'),
            ('Inflation', 'Competition of market price')
        ])
            
        # Buyer Capability CPD
        cpd_buyer_capability = TabularCPD(variable='buyer_capability', variable_card=2,
                                        values=[[0.8], [0.2]])

        # Market Competition CPD
        cpd_market_competition = TabularCPD(variable='market_competition', variable_card=2,
                                            values=[[0.6, 0.4], [0.4, 0.6]],
                                            evidence=['buyer_capability'],
                                            evidence_card=[2])

        # Seller Competition Capability CPD
        cpd_seller_competition_capability = TabularCPD(variable='seller_competition_capability', variable_card=2,
                                                    values=[[0.7], [0.3]])

        # Negotiation Deadline Pressure CPD
        cpd_negotiation_deadline_pressure = TabularCPD(variable='negotiation_deadline_pressure', variable_card=2,
                                                    values=[[0.5, 0.7, 0.6, 0.8], [0.5, 0.3, 0.4, 0.2]],
                                                    evidence=['market_competition', 'seller_competition_capability'],
                                                    evidence_card=[2, 2])

        # Offer Price CPD
        cpd_offer_price = TabularCPD(variable='offer_price', variable_card=2,
                                    values=[[0.4, 0.6], [0.6, 0.4]],
                                    evidence=['negotiation_deadline_pressure'],
                                    evidence_card=[2])

        # Add CPDs to the model
        model.add_cpds(cpd_buyer_capability, cpd_market_competition, cpd_seller_competition_capability,
                    cpd_negotiation_deadline_pressure, cpd_offer_price)

        # Validate the model
        assert model.check_model()

    def create_seller_network():
        """ This function builds the bayesian network for the seller, and returns an external factor value [0,1]
        """
        pass