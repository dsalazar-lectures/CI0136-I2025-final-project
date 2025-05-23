from .types import INotificationService
from .factories import IBuilderFactory

class EmailService():
    def __init__(self, IBuilderFactory: IBuilderFactory, INotificationService: INotificationService):
        self.factory = IBuilderFactory
        self.smtp_service = INotificationService
    
    def send_email(self, builder_type: str, data: dict) -> bool:
        # Create the email body using the factory
        try:
            builder = self.factory.create_builder(builder_type)
        except ValueError as e:
            print(f"Error creating builder: {e}")
            return False
        
        try:
            email_body = builder.build_body(data)
        except Exception as e:
            print(f"Error building email body: {e}")
            return False
        
        # Send the email using the SMTP service
        try:
            return self.smtp_service.send(email_body)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
