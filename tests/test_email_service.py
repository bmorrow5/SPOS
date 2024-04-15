import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import unittest
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService
from backend.data_service.models import ProductDatabase

class TestEmailService(unittest.TestCase):
    """Tests the functionality of the email service
    """

    def setUp(self):
        self.email_service = EmailService(first_name= "John", last_name="Doe", email='spos6045@gmail.com', password='cjoisegsetxkqdxb')

    # def test_request_quotes(self):        
    #     ds = DataService()
    #     # Get the product
    #     product = ds.read_product(product_id=1)
    #     # Call the method
    #     result = self.email_service.request_quotes(product=product)
    #     # Asserts
    #     self.assertTrue(result)

    def test_read_emails(self):
        result = self.email_service.read_emails()
        print(result)
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()