# Biblioteca para la clase abstracta
from abc import ABC, abstractmethod

class EmailNotifier(ABC):

    @abstractmethod
    def send(self, user, builder_type: str):
        pass


class SMTPNotifier(EmailNotifier):
    def send(self, user, builder_type: str):
        #factory = body_factories.EmailBuilderFactory()
        #smtp_service = email_service.SMTPEmailService()
        #builder = factory.createBody(builder_type)
        #notification_data = builder.buildBody()
        #email_to = user["email"]
        #return smtp_service.send_email(email_to, notification_data["subject"], notification_data["body"])
        pass