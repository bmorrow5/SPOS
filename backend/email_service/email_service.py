import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from data_service.data_service import DataService


class EmailService():
    """This class will handle sending emails to suppliers and reading emails from suppliers
    It is built to work with gmail accounts only
    """
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587  
        self.imap_server = "imap.gmail.com" 


    def send_email(self, to_email: list, subject: str, message: str) -> str:
        """ This will send an email from a gmail account to a list of emails
        """
        try:
            if subject is None:
                subject = "No Subject"
            if message is None:
                message = "No Message"

            for email in to_email:
                # Setup the email
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.email, self.password)
                    text = msg.as_string()
                    server.sendmail(self.email, email, text)
                return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
        


    def request_quotes(self, product, message=None) -> bool:
        """Emails to request initial quotes. The subject line will have the product name and game_id, and the 
            message will be a generic message if none is provided.
       Args:
            email_list (list): Suppliers to send email to
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents
            Product (Product): Product to request quotes for

        Returns:
            bool: True if emails sent, False if failed
        """
        try:
            # Lets first use our data service to get all our sellers, and start an instance of a game.
            ds = DataService()
            sellers = ds.read_all_sellers()
            buyer = ds.read_buyer(first_name=self.first_name, last_name=self.last_name, email=self.email)
        
            # If message is none make a custom message for each seller
            if message is None:
                message = f"To Whom It May Concern,\n\nWe are requesting a quote for {product.quantity} {product.name}s.\n\nPlease reply to this email with your best price, and in the body of the email not on an attachment. \n\nThank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
            
            for seller in sellers:

                # Declare a new game
                game_id = ds.create_game(seller_id = seller.seller_id, 
                                      buyer_agent_id = buyer.buyer_agent_id, 
                                      product_id= product.product_id, 
                                      buyer_reservation_price= product.max_price)

                # We will use the game id to identify the game when replying to emails later
                subject = f"Request for Quote - {product.quantity} {product.name}s - ID: ({game_id})"
                EmailService.send_email(self, [seller.email], subject, message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False


    def check_email(self):
        try:
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(self.imap_server) as mail:
                mail.login(self.email, self.password)
                mail.select('inbox')  # Connect to inbox

                # Search for all emails
                status, messages = mail.search(None, 'All')
                if status != 'OK':
                    print("No emails found!")
                    return

                # Process emails
                for num in messages[0].split():
                    status, data = mail.fetch(num, '(RFC822)')
                    if status != 'OK':
                        print("ERROR getting message", num)
                        return

                    # Parse email content
                    msg = email.message_from_bytes(data[0][1])
                    print('From:', msg['From'])
                    print('Subject:', msg['Subject'])
                    print("Message:", msg.get_payload(decode=True))

            mail.close()
            mail.logout()
        except Exception as e:
            print(f"Failed to read emails: {e}")



