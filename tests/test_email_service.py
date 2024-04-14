import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import unittest
from unittest.mock import patch, MagicMock
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService
from backend.data_service.models import ProductDatabase

class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.email_service = EmailService('spos6045@gmail.com', 'cjoisegsetxkqdxb')

    @patch('smtplib.SMTP')
    def test_request_quotes(self, mock_smtp):        
        # New product
        product = ProductDatabase(name="Office Chairs", quantity= 100.0, max_price= 100.0, date_needed_by= "2021-12-12")

        # Call the method
        result = self.email_service.request_quotes('subject', 'message', product)

        # Asserts
        self.assertEqual(result, True)

if __name__ == '__main__':
    unittest.main()