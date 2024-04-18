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
        buyer_network = BayesianNetwork([
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
        ])
            
        # Buyer Capability CPD, need to add the rest
        cpd_buyer_capability = TabularCPD(variable='buyer_capability', variable_card=2,
                                        values=[[0.8], [0.2]])


        buyer_network.add_cpds(cpd_buyer_capability)

        # Validate the model
        assert buyer_network.check_model()

    def create_seller_network():
        """ This function builds the bayesian network for the seller, and returns an external factor value [0,1]
        """
        seller_network = BayesianNetwork([
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