import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(1, parent_dir)
import smtplib
import imaplib
import email
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from data_service.data_service import DataService


class EmailService():
    """This class will handle sending emails to suppliers and reading emails from suppliers
    It is built to work with gmail accounts only, and will be modified later to work with others
    """
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587  
        self.imap_server = "imap.gmail.com" 


    def send_emails(self, to_emails: list, subject: str, message: str) -> str:
        """ This will send an email from a gmail account to a list of emails
        """
        try:
            if subject is None:
                subject = "No Subject"
            if message is None:
                message = "No Message"

            for email in to_emails:
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
        

    def read_emails(self, type="Unseen"):
        """This will read all or unread emails depending on type

        Args:
            type (str): All or Unread. Defaults to "Unread".

        Returns:
            Message: The email messages
        """
        try:
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(self.imap_server) as mail:
                mail.login(self.email, self.password)
                mail.select('inbox')  # Connect to inbox
                msg = None
                # Search for all emails
                status, messages = mail.search(None, type)
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
                    # print('From:', msg['From'])
                    # print('Subject:', msg['Subject'])
                    # print("Message:", msg.get_payload(decode=True))
                mail.close()
                mail.logout()
            if msg is None:
                return "No emails found"
            else:
                return msg
        except Exception as e:
            print(f"Failed to read emails: {e}")




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
                message = f"To Whom It May Concern,\n\nWe are requesting a quote for {product.quantity} {product.name}s.\n\nPlease reply to this email with your best price, and in the body of the email, not on an attachment. \n\nThank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
            
            # Iterate through all sellers in the database
            for seller in sellers:

                # Declare a new game
                game_id = ds.create_game(seller_id = seller.seller_id, 
                                      buyer_agent_id = buyer.buyer_agent_id, 
                                      product_id= product.product_id, 
                                      buyer_reservation_price= product.max_price)

                # We will use the game id to identify the game when replying to emails later
                subject = f"Request for Quote - {product.quantity} {product.name}s - Request ID: ({game_id})"
                EmailService.send_emails(self, [seller.email], subject, message)
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False




    def reply_with_counteroffer(self, to_emails: list, counter_offer_price: float, message: str, original_message_id: str) -> str:
        """This will reply with a counteroffer to the supplier with the price found by the bayesian game theory model

        Args:
            from_email (str): _description_
            to_emails (list): _description_
            counter_offer_price (float): _description_
            subject (str): _description_
            message (str): _description_

        Returns:
            str: Success or failure message
        """

        try:
            if message is None:
                message = f"Please see our counteroffer of {counter_offer_price}" 
            for email in to_emails:
                # Setup the email
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = email
                msg['In-Reply-To'] = original_message_id
                # msg['References'] = original_message_id
                msg['Subject'] = "Counter Offer"
                msg.attach(MIMEText(message, 'plain'))

                # Connect to the server and send the email
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                try:
                    server.login(self.email, self.password)
                except Exception as e:
                    print(f"Failed to login: {e}")
                text = msg.as_string()
                server.sendmail(self.email, email, text)
                server.quit()
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")


    def send_acceptance(self, to_email: str, message: str) -> str:
        """This will send an email accepting the offer

        Args:
            to_email (str): Email to send to
            message (str): Message to send
            original_message_id (str): Original message id

        Returns:
            str: Success or failure message
        """
        message = f"To Whom It May Concern,\n\nThank you for your offer we accept.\n\nThank you,\n\n{self.first_name} {self.last_name}\nYour Company Intl."
        
        self.send_emails(to_emails=[to_email], subject="Acceptance", message=message)



    def extract_game_id_and_price(self, subject, content):
        """This will extract the game_id and offer price from the email subject and content

        Args:
            subject (string): Email subject
            content (string): Content of the email

        Returns:
            dict: game_id and offer_price
        """
        # Regex to extract game_id from the subject
        game_id_pattern = r"Request ID: \((\d+)\)"
        # Regex to extract offer_price, $123.45 or 123.45$
        price_pattern = r"\$?(\d+\.\d{2})\$?"

        game_id_match = re.search(game_id_pattern, subject)
        price_match = re.search(price_pattern, content)

        if game_id_match is not None:
            game_id = game_id_match.group(1)
        else:
            game_id = None

        if price_match is not None:
            offer_price = price_match.group(1)
        else:
            offer_price = None

        return {game_id, offer_price}


    def update_games(self, game_id, offer_price):
        """This will update the game with the offer price

        Args:
            game_id (int): Game id
            offer_price (float): Offer price
        """
        ds = DataService()
        messages = self.read_emails()

        for message in messages:
            game_id, offer_price = self.extract_game_id_and_price(message['subject'], message.get_payload(decode=True))
            ds.update_game(game_id, offer_price)
        
        ds.update_game(game_id=game_id, offer_price)

