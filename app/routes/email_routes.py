from flask import Blueprint, render_template, request
from app.models.services import email_service
from app.models.builders import body_factories
from app.controllers.email_controller import send_email

mail_bp = Blueprint('mail_bp',
                    __name__,
                    template_folder='../templates')

@mail_bp.route('/email')
def index():
  return render_template("sendmailbtn.html")

@mail_bp.route("/send", methods=["POST"])
def enviar():
  to = request.form.get("email")

  factory = body_factories.EmailBuilderFactory()
  service = email_service.SMTPEmailService()

  return send_email(factory.createBody("login"), to, service)