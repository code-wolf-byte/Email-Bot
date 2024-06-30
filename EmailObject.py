import uuid
class Email():

    def __init__(self, sender, subject, body, attachments, channel, recipient = None ):
        self.sender = sender
        self.recipient = recipient
        self.subject = subject
        self.body = body
        self.attachments = attachments
        self.channel = channel
        self.id = uuid.uuid4()
        self.response = None
        self.responseFiles = []
        self.responseSubject = None
    def getSender(self):
        return self.sender
    def getRecipient(self):
        return self.recipient
    def getSubject(self):
        return self.subject
    def getBody(self):
        return self.body
    def getAttachments(self):
        return self.attachments
    def getChannel(self):
        return self.channel
    def setResponse(self, response):
        self.response = response
    def setResponseFiles(self, responseFiles):
        self.responseFiles = responseFiles
    def setReponseSubject(self, subject):
        self.responseSubject = subject
    def __str__(self):
        return f"From: {self.sender}\nTo: {self.recipient}\nSubject: {self.subject}\nBody: {self.body}\nAttachments: {self.attachments}"

    