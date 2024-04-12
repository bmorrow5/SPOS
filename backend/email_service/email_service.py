import smtplib
import imaplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailService:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587  
        self.imap_server = "imap.gmail.com" 

    def send_counteroffer(self, from_email: str, to_emails: list, counter_offer_price: float, subject: str, message: str) -> str:
        """Emails a supplier a counteroffer with the price found by the bayesian game theory model

        Args:
            from_email (str): Employee sending the email
            to_email (list): Supplier receiving updated price
            counter_offer_price (float): Bayesian Games counter_offer_price
            subject (str): Email subject
            message (str): Email contents

        Returns:
            str: confirmation email was sent
        """
        
        try:
            if subject is None:
                subject = "Counter Offer"
            if message is None:
                message = "Please see our attached counteroffer" 
            for email in to_emails:
                # Setup the email
                msg = MIMEMultipart()
                msg['From'] = from_email
                msg['To'] = email
                msg['Subject'] = subject
                msg.attach(MIMEText(message, 'plain'))

                # Connect to the server and send the email
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.starttls()
                server.login(self.email, self.password)
                text = msg.as_string()
                server.sendmail(from_email, to_emails, text)
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

    def request_bids(self):
        pass
