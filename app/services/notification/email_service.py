from app.services.notification.smtp_email_type import SMTPEmailService
from app.services.notification.factories.email_factory import EmailBuilderFactory

class Emailservice():
    def __init__(self):
        self.factory = EmailBuilderFactory()
        self.smtp_service = SMTPEmailService()
    
    def send_email(self, builder_type: str, data: dict):
        # Create the email body using the factory
        builder = self.factory.createBody(builder_type)
        email_body = builder.buildBody(data)
        
        # Send the email using the SMTP service
        self.smtp_service.send(email_body)