import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

class EmailSender:
    def __init__(self, email, password):
        self.email = email
        self.password = password

    def send_email(self, recipient, subject, body, attachments=None):
        msg = MIMEMultipart()
        msg['From'] = self.email
        msg['To'] = recipient
        msg['Subject'] = subject
        msg.attach(MIMEText(body))
        
        if attachments:
            for attachment in attachments:
                if (attachment != 'message.txt'):
                    with open(attachment, "rb") as f:
                        part = MIMEBase(f.read(), name = os.path.basename(attachment))
                    part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(attachment)
                    msg.attach(part)

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(self.email, self.password)
        server.sendmail(self.email, recipient, msg.as_string())
        server.quit()
        
        if attachments:
            for attachment in attachments:
                os.remove(attachment)