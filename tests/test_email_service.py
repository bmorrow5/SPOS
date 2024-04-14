import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import unittest
from unittest.mock import patch, MagicMock
from backend.email_service.email_service import EmailService
from backend.data_service.data_service import DataService

class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.email_service = EmailService('spos6045@gmail.com', 'cjoisegsetxkqdxb')

    @patch('smtplib.SMTP')
    def test_request_quotes(self, mock_smtp):
        # Setup mock
        server_mock = MagicMock()
        mock_smtp.return_value = server_mock
        
        # New product
        product = {
            "product_name": "Office Chairs",
            "buyer_agent_id": 1,
            "quantity": 100.0,
            "product_quantity": 100.0,
            "max_price": 100.0,
            "date_needed_by": "2021-12-12",
        }



        # Call the method
        result = self.email_service.request_quotes('subject', 'message', 'Product')

        # Asserts
        self.assertEqual(result, "Email sent successfully!")
        server_mock.starttls.assert_called_once()
        server_mock.login.assert_called_once_with('spos6045@gmail.com', 'cjoisegsetxkqdxb')
        server_mock.sendmail.assert_called_once()
        server_mock.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()