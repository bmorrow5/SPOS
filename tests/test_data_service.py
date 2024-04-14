import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.data_service.models import Base, SellerDatabase, BuyerAgentDatabase
from backend.data_service.data_service import DataService 

class TestDataService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to an in-memory SQLite database for testing
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.data_service = DataService()
        cls.data_service.Session = cls.Session  # Override the sessionmaker with the test session

    def setUp(self):
        # Start a transaction before each test method
        self.transaction = self.engine.begin()
        self.session = self.Session(bind=self.transaction)

    def tearDown(self):
        # Rollback the transaction after each test method
        self.session.close()
        self.transaction.rollback()

    def test_create_seller(self):
        self.data_service.create_seller("John Doe", "john@example.com")
        seller = self.session.query(SellerDatabase).filter_by(name="John Doe").one_or_none()
        self.assertIsNotNone(seller)
        self.assertEqual(seller.email, "john@example.com")

    def test_read_seller(self):
        self.data_service.create_seller("Jane Doe", "jane@example.com")
        seller = self.data_service.read_seller(name="Jane Doe")
        self.assertIsNotNone(seller)
        self.assertEqual(seller.email, "jane@example.com")

    def test_update_seller_email(self):
        self.data_service.create_seller("Alice Doe", "alice@example.com")
        self.data_service.update_seller_email(name="Alice Doe", email="newalice@example.com")
        updated_seller = self.data_service.read_seller(name="Alice Doe")
        self.assertEqual(updated_seller.email, "newalice@example.com")

    def test_delete_seller(self):
        self.data_service.create_seller("Bob Doe", "bob@example.com")
        delete_status = self.data_service.delete_seller(name="Bob Doe")
        self.assertTrue(delete_status)
        seller = self.data_service.read_seller(name="Bob Doe")
        self.assertIsNone(seller)

    # You can add similar tests for buyers, products, games, and email logs

if __name__ == '__main__':
    unittest.main()
