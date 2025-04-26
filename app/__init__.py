from flask import Flask, render_template, request
from app.models.services import email_service
from app.models.builders import email_notification_builders
from app.controllers.email_controller import send_email

def create_app():
    app = Flask(__name__)
    app.secret_key = "secreto"

    @app.route("/")
    def index():
        return render_template("sendmailbtn.html")

    @app.route("/enviar", methods=["POST"])
    def enviar():
        to = request.form.get("email")
        service = email_service.SMTPEmailService()
        builder = email_notification_builders.loginEmailBuilder()
        return send_email(builder, to, service)

    return app
