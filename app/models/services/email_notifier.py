# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod
from app.models.builders.body_factories import BodyFactory
from app.models.services.email_service import EmailService
from app.models.services import email_service
from app.models.builders.email_notification_builders import Builder
from app.models.builders import body_factories

class EmailNotifier(ABC):

    @abstractmethod
    def send(self, user, builder_type: str):
        pass


class SMTPNotifier(EmailNotifier):
    def send(self, user, builder_type: str):
        factory = body_factories.EmailBuilderFactory()
        smtp_service = email_service.SMTPEmailService()
        builder = factory.createBody(builder_type)
        notification_data = builder.buildBody()

        #User's email address based on the logged in user. Session required
        #email_to = user.mail 
        #return smtp_service.send_email(email_to, notification_data["subject"], notification_data["body"])
