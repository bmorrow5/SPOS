from pgmpy.models import BayesianNetwork
from pgmpy.factors.discrete import TabularCPD


class GameBayesianNetwork():

    def __init__(self):
        None

    def create_network():
        model = BayesianNetwork([
        ('buyer_capability', 'market_competition'),
        ('market_competition', 'negotiation_deadline_pressure'),
        ('seller_competition_capability', 'market_competition'),
        ('negotiation_deadline_pressure', 'offer_price'),
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