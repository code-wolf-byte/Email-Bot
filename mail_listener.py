import email as email_module
import imaplib
import os

class EmailListener:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL('imap.gmail.com')
        self.mail.login(self.username, self.password)
        self.setup = False
    
    def setupBot(self):
        self.setup = True
    
    def isSetup(self):
        return self.setup
    
    def parse_email(self, msg):
        sender =email_module.utils.parseaddr(msg['From'])[1]
        subject = msg['Subject']
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get('Content-Disposition'))
                if ctype == 'text/plain' and 'attachment' not in cdispo:
                    body = part.get_payload(decode=True)
                    break
        else:
            body = msg.get_payload(decode=True)
        attachments = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            filename = part.get_filename()
            if filename:
                attachments.append(part)
        return sender, subject, body, attachments
    
    def listen(self):
        self.mail.select("inbox")
        status, emails = self.mail.search(None, "UNSEEN")
        emails = emails[0].split()
        unread_emails = []
        for email_id in emails:
            status, email_data = self.mail.fetch(email_id, "(RFC822)")
            for response in email_data:
                if isinstance(response, tuple):
                    msg = email_module.message_from_bytes(response[1])
                    sender, subject, body, attachments = self.parse_email(msg)
                    email = {"sender":sender, "subject": subject, "body": body, "attachments": attachments}
                    email['body'] = str(email['body'])[2:-1]
                    email['body'] = email['body'].replace("\\r\\n", " ")
                    email['body'] = email['body'].replace("\\n", " ")
                    email['body'] = email['body'].replace("\\x92", "'")

                    unread_emails.append(email)
        return unread_emails


    def removeASCII(self,  text):
        dictonary = { '\\x92', "'", '\\xf0', '' }
        for element in dictonary:
            text = text.replace(element, dictonary[element])