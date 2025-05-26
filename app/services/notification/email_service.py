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
        # Crea un builder utilizando un factory
        try:
            builder = self.factory.create_builder(builder_type)
        except ValueError as e:
            print(f"Error creating builder: {e}")
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
