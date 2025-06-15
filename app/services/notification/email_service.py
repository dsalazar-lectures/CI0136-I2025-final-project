from flask import session
from .types import INotificationService
from .factories import IBuilderFactory

class EmailService():
    """
    Clase EmailService
    Esta clase se encarga de enviar correos electronicos utilizando el servicio SMTP.

    Atributos:
        factory (IBuilderFactory): Instancia de la fabrica de builders.
        notification_service (INotificationService): Instancia del servicio de notificacion.
    """
    def __init__(self, IBuilderFactory: IBuilderFactory, INotificationService: INotificationService):
        self.factory = IBuilderFactory
        self.notification_service = INotificationService
    

    def send_email(self, builder_type: str, data: dict) -> bool:
        """
        builder_type: tipo de notificación que se quiere enviar, (Login, Reminder, etc).\n
        data: diccionario que se debe pasar para poder crear el cuerpo de la notificación,
            depende del tipo de notificación,ver la documentación.
        """
        
        # Necesario retornar False en caso de que no exista session, exclusivo del caso de recuperar pass. 
        notification_enabled = session.get("notification_enabled", False)

        # Crea un builder utilizando un factory
        try:
            builder = self.factory.create_builder(builder_type)
        except ValueError as e:
            print(f"Error creating builder: {e}")
            return False

        # Valida si las notificaciones están deshabilitadas y si el builder no es de tipo obligatorio de notificar
        if not notification_enabled and not builder.get_bypass_priority():
            return False    
    
        # Construye el cuerpo del correo
        try:
            email_body = builder.build_body(data)
        except Exception as e:
            print(f"Error building email body: {e}")
            return False
        
        # Envía el correo usando SMTP
        try:
            return self.notification_service.send(email_body)
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
