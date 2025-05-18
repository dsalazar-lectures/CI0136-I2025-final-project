from flask import redirect, url_for, flash, request
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import Builder
from app.models.services import email_service
from app.models.services import password_service
from app.models.services import email_notifier


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
     flash("Las contraseñas no coinciden", "error")
     return redirect("/change_password")
    else:
        service = password_service.ChangePasswordService()
        notifier = email_notifier.SMTPNotifier()
        valid_password = service.validate_password(new_password_input)
        #Pepito since there's still no user, a valid logged in user must be passed through the method
        if (valid_password and service.change_password(current_password_input, new_password_input, "Pepito Salazar")):
            flash("Contraseña cambiada exitosamente", "success")

            '''
            #LOGIC TO SEND EMAIL AFTER CHANGING THE PASSWORD. USER SESSION REQUIRED
            if (notifier.send(user, "changepassword")):
               #el correo se envio exitosamente
            else:
               #el correo no se envio exitosamente
            '''   
        else: 
            if (valid_password):
                flash("La actual contraseña ingresada no es valida", "error") #the current password specified is not the one stored in the DB
            else: 
               flash("La contraseña debe tener 8 caracteres, mayuscula, minuscula y simbolos", "error") #the password doesn't meet the standars
        return redirect("/change_password")