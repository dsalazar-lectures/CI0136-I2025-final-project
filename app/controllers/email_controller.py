from flask import redirect, url_for, flash
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import EmailBuilder

def send_email(builder: EmailBuilder, user_email:str, service: EmailService):
  email_data = builder.buildBody();
  sent = service.send_email(user_email, email_data["subject"], email_data["body"]);

  if (sent):
    flash("Correo enviado con éxito")
  else:
    flash("Error al enviar el correo")

  return redirect(url_for("index"))