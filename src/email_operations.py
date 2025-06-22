from smtplib import SMTP, SMTPException
import imaplib
import email
import json
import os

class EmailOperations:
    def __init__(self, email_address: str, password: str):
        self.email_address = email_address
        self.password = password
        self.imap_server = 'imap.gmail.com'
        self.smtp_server = 'smtp.gmail.com'
        self.whitelist_file = 'data/whitelist.txt'

    def connect_to_email(self):
        try:
            self.mail = imaplib.IMAP4_SSL(self.imap_server)
            self.mail.login(self.email_address, self.password)
            return True
        except SMTPException as e:
            self.log_error(f"Failed to connect to email: {e}")
            return False

    def fetch_inbox(self):
        try:
            self.mail.select('inbox')
            result, data = self.mail.search(None, 'ALL')
            email_ids = data[0].split()
            emails = []
            for email_id in email_ids:
                result, msg_data = self.mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append({
                    'subject': msg['subject'],
                    'from': msg['from'],
                    'date': msg['date'],
                    'body': self.get_email_body(msg)
                })
            return emails
        except Exception as e:
            self.log_error(f"Failed to fetch inbox: {e}")
            return []

    def get_email_body(self, msg):
        if msg.is_multipart():
            return ''.join(part.get_payload(decode=True).decode() for part in msg.walk() if part.get_content_type() == 'text/plain')
        else:
            return msg.get_payload(decode=True).decode()

    def add_to_whitelist(self, email_address: str):
        if not self.is_in_whitelist(email_address):
            with open(self.whitelist_file, 'a') as f:
                f.write(email_address + '\n')

    def is_in_whitelist(self, email_address: str) -> bool:
        if os.path.exists(self.whitelist_file):
            with open(self.whitelist_file, 'r') as f:
                return email_address in f.read().splitlines()
        return False

    def log_error(self, message: str):
        with open('data/error_logs.txt', 'a') as f:
            f.write(f"{message}\n")