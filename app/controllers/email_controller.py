from flask import redirect, url_for, flash
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import Builder

def send_email(builder: Builder, to: str, service: EmailService):
  notification_data = builder.buildBody();
  sent = service.send_email(to, notification_data["subject"], notification_data["body"]);

  if (sent):
    flash("Correo enviado con éxito")
  else:
    flash("Error al enviar el correo")

  return redirect(url_for("index"))