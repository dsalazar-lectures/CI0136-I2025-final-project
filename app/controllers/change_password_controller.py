from flask import redirect, url_for, flash, request
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import Builder
from app.models.services import email_service
from app.models.services import password_service
from app.models.builders import body_factories

from flask import Blueprint, render_template

c_password_bp = Blueprint('cpassword', __name__)

@c_password_bp.route("/change_password")
def index():
  return render_template("change_password.html")


@c_password_bp.route("/change_pass", methods=["POST"])
def change_pass():
    current_password_input = request.form.get("current_password")
    new_password_input = request.form.get("new_password")
    confirm_password_input = request.form.get("confirm_password")

    if new_password_input != confirm_password_input:
     flash("Las nuevas contraseñas no coinciden", "error")
     return redirect("/change_password")
    else:
        factory = body_factories.EmailBuilderFactory()
        service = password_service.password_service()
        if (service.change_password(current_password_input, new_password_input)):
            flash("Contraseña cambiada exitosamente", "success")
        else: 
            flash("Error al cambiar la contraseña", "error")     
        #return redirect("/")
        return redirect("/change_password")