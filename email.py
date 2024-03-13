class Email:
    def __init__(self, sender, receiver, subject, message):
        self.sender = sender
        self.receiver = receiver
        self.subject = subject
        self.message = message

    def send_email(self):
        print(f"From: {self.sender}")
        print(f"To: {self.receiver}")
        print(f"Subject: {self.subject}")
        print(f"Message: {self.message}")