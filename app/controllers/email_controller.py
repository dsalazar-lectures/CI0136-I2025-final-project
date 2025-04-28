from flask import redirect, url_for, flash, request
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import Builder
from app.models.services import email_service
from app.models.builders import body_factories

from flask import Blueprint, render_template

mail_bp = Blueprint('email', __name__)

@mail_bp.route("/enviarnotificacion")
def index():
  return render_template("sendmailbtn.html")

@mail_bp.route("/enviar", methods=["POST"])
def enviar():
  to = request.form.get("email")

  factory = body_factories.EmailBuilderFactory()
  service = email_service.SMTPEmailService()

  return send_email(factory.createBody("login"), to, service)

def send_email(builder: Builder, to: str, service: EmailService):
  notification_data = builder.buildBody()
  sent = service.send_email(to, notification_data["subject"], notification_data["body"])

  if (sent):
    flash("Correo enviado con éxito")
  else:
    flash("Error al enviar el correo")

  return redirect("/")

