import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from backend.data_service.data_service import DataService


class EmailService():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587  
        self.imap_server = "imap.gmail.com" 


    def send_counteroffer(self, from_email: str, to_email: list, counter_offer_price: float, message: str, original_message_id: str) -> str:
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
            for email in to_email:
                # Setup the email
                msg = MIMEMultipart()
                msg['From'] = from_email
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

    def request_quotes(self, subject: str, message: str, Product: object) -> str:
        """Emails to request initial quotes
       Args:
            email_list (list): Suppliers to send email to
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents
            Product (Product): Product to request quotes for

        Returns:
            str: confirmation email was sent
        """
        
        try:
            sellers = DataService.read_all_sellers()
            if subject is None:
                subject = "Request for Quote"
            if message is None:
                message = f"We are requesting a quote for the following product: {Product.name} in the quanity of {Product.quantity}"

            for seller in sellers:
                # Setup the email
                msg = MIMEMultipart()
                msg['From'] = self.email
                msg['To'] = seller.email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                # Connect to the server and send the email
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email, self.password)
                text = msg.as_string()
                server.sendmail(self.email, seller.email, text)
                server.quit()
                print("Email sent successfully!")
        except Exception as e:
            print(f"Failed to send email: {e}")



    def check_email_for_offers(self):
        try:
            # Connect to IMAP server
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.email, self.password)
            mail.select('inbox')  # Connect to inbox

            # Search for all emails
            status, messages = mail.search(None, 'ALL')
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