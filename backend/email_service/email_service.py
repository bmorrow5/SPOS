import smtplib
import imaplib
import email
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class EmailService():
    """This class will handle sending emails to suppliers and reading emails from suppliers
    It is built to work with gmail accounts only, and will be modified later to work with others
    """
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.smtp_server = "smtp.gmail.com"  
        self.smtp_port = 587  
        self.imap_server = "imap.gmail.com" 


    def send_emails(self, to_emails: list, subject: str, message: str, in_reply_to=None, refrences=None) -> str:
        """ This will send an email from a gmail account to a list of emails
        It can also reply to emails
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

                if in_reply_to is not None:
                    msg['In-Reply-To'] = in_reply_to
                if refrences is not None:
                    msg['References'] = refrences

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
        email_details = []
        try:
            # Connect to IMAP server
            with imaplib.IMAP4_SSL(self.imap_server) as mail:
                mail.login(self.email, self.password)
                mail.select('inbox')  # Connect to inbox
                msg = None
                # Search for all emails
                status, messages = mail.search(None, type)
                if status != 'OK':
                    print("No emails found")
                    return
                # Process emails
                for num in messages[0].split():
                    status, data = mail.fetch(num, '(RFC822)')
                    if status != 'OK':
                        print("ERROR getting message", num)
                        return

                    # Parse email content
                    msg = email.message_from_bytes(data[0][1])

                    email_detail = {
                        'from': msg['From'],
                        'subject': msg['Subject'],
                        'content': msg.get_payload(decode=True),  # 'payload' is the message content
                        'message_id': msg['Message-ID'],
                        'references': msg['References'],
                        'in_reply_to': msg['In-Reply-To']
                    }
                    email_details.append(email_detail)
                mail.close()
                mail.logout()
                
            if msg is None:
                return "No emails found"
            else:
                return email_details
        except Exception as e:
            print(f"Failed to read emails: {e}")


