import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import unittest
from unittest.mock import patch, MagicMock
from backend.email_service.email_service import EmailService

class TestEmailService(unittest.TestCase):
    def setUp(self):
        self.email_service = EmailService('spos6045@gmail.com', 'cjoisegsetxkqdxb')

    @patch('smtplib.SMTP')
    def test_send_counteroffer_success(self, mock_smtp):
        # Setup mock
        server_mock = MagicMock()
        mock_smtp.return_value = server_mock
        
        # Call the method
        result = self.email_service.send_counteroffer('spos6045@gmail.com', ['brandonmorrow09@gmail.com'], 100.0, 'Please consider our counteroffer.', 'original-msg-id')

        # Asserts
        self.assertEqual(result, "Email sent successfully!")
        server_mock.starttls.assert_called_once()
        server_mock.login.assert_called_once_with('spos6045@gmail.com', 'cjoisegsetxkqdxb')
        server_mock.sendmail.assert_called_once()
        server_mock.quit.assert_called_once()


    @patch('smtplib.SMTP')
    def test_send_counteroffer_failure(self, mock_smtp):
        # Setup mock to raise an exception
        server_mock = MagicMock()
        server_mock.login.side_effect = Exception("Login failed")
        mock_smtp.return_value = server_mock

        # Call the method
        result = self.email_service.send_counteroffer('spos6045@gmail.com', ['brandonmorrow09@gmail.com'], 100.0, 'Please consider our counteroffer.', 'original-msg-id')

        # Asserts
        self.assertIn("Failed to send email:", result)
        server_mock.quit.assert_called_once()

if __name__ == '__main__':
    unittest.main()