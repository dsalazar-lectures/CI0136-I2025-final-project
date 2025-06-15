from abc import ABC, abstractmethod
from .email_service import SMTPEmailService

class BanNotification(SMTPEmailService):
  def __init__(self):
    super().__init__()
    self.subject = "Notificación de Baneo"
  
  def notify(self,to):
    return self.send_email(to,self.subject,self.message)


class BehavioralViolation(BanNotification):
  def __init__(self):
    super().__init__()
    self.message = "Su cuenta ha sido suspendida debido a una violación en las reglas de comportamiento de nuestro servicio"

class DefaultPayments(BanNotification):
  def __init__(self):
    super().__init__()
    self.message = "Su cuenta ha sido suspendida debido al incumplimiento con el tiempo de los pagos"

class ViolationTerms(BanNotification):
    def __init__(self):
      super().__init__()
      self.message = "Su cuenta ha sido suspendida debido a una violación en los términos y condiciones del sitio"

class Fraud(BanNotification):
  def __init__(self):
    super().__init__()
    self.message = "Su cuenta ha sido suspendida debido a fraude con la información añadida a los datos personales"

class ilegalContent(BanNotification):
  def __init__(self):
    super().__init__()
    self.message = "Su cuenta ha sido suspendida debido a la publicación de contenido que rompe con nuestras reglas"
  

class BanNotificationFactory:

    @staticmethod
    def create_ban_notification(bantype: str) -> BanNotification:
        if bantype == "behavior":
            return BehavioralViolation()
        elif bantype == "payments":
            return DefaultPayments()
        elif bantype == "termsV":
            return ViolationTerms()
        elif bantype == "Fraud":
           return Fraud()
        elif bantype == "content":
           return ilegalContent()
        else:
            raise ValueError("Invalid ban type")

    