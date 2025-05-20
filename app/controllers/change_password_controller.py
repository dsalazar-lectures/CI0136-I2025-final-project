from flask import redirect, url_for, flash, request, session
from app.models.services.email_service import EmailService
from app.models.builders.email_notification_builders import Builder
from app.models.services import email_service
from app.models.services import password_service
from app.models.services import email_notifier
from app.models.repositories.users import firebase_user_repository

####################################################
# THIS ONLY WORKS IF THERE'S AN ACTIVA SESSION
####################################################


from flask import Blueprint, render_template

c_password_bp = Blueprint('cpassword', __name__)

repo = firebase_user_repository.FirebaseUserRepository()

@c_password_bp.route("/change_password")
def index():
  #this works only if there's an active session
  if session:
    user = repo.get_user_by_id(session["user_id"])   
    return render_template("change_password.html", user_name=user["name"])
  else:
     return redirect("/")


@c_password_bp.route("/change_pass", methods=["POST"])
def change_pass():
    
    current_password_input = request.form.get("current_password")
    new_password_input = request.form.get("new_password")
    confirm_password_input = request.form.get("confirm_password")

    if new_password_input != confirm_password_input:
     flash("Las contraseñas no coinciden", "error")
     return redirect("/change_password")
    else:
        user = repo.get_user_by_id(session["user_id"])

        service = password_service.ChangePasswordService()
        notifier = email_notifier.SMTPNotifier()

        valid_password = service.validate_password(new_password_input)

        if (valid_password and service.change_password(current_password_input, new_password_input, user)):
            flash("Contraseña cambiada exitosamente", "success")

            
            #Notify by email after changing the password
            print("correo enviado") if notifier.send(user, "changepassword") else print("error")
               
        else: 
            if (valid_password):
                flash("La actual contraseña ingresada no es valida", "error") #the current password specified is not the one stored in the DB
            else: 
               flash("La contraseña debe tener 8 caracteres, mayuscula, minuscula y simbolos", "error") #the password doesn't meet the standars
        return redirect("/change_password")