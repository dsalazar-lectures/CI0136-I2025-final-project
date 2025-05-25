from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.services import email_notifier
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
# Para crear token firmado
from itsdangerous import URLSafeTimedSerializer
# Para enviar correo
from app.services.notification import send_email_notification
# Para logs
from app.services.audit import log_audit, AuditActionType

repo = FirebaseUserRepository()

rec_password_bp = Blueprint('recoveryPassword', __name__)

@rec_password_bp.route("/recovery_password", methods=['GET'])
def recoveryPasswordView(): 
    return render_template("recovery_password.html")

@rec_password_bp.route("/recovery_password", methods=['POST'])
def recover():
    userEmail = request.form.get('email')
    
    if userEmail:
        user = repo.get_user_by_email(userEmail)
        if user:
            token = generate_password_reset_token(userEmail)
            reset_link = url_for('recoveryPassword.reset_password_form', token=token, _external=True)
            
            # Prepare email data for notification
            email_data = {
                "username": user.get("name", "Usuario"),
                "emailTo": userEmail,
                "reset_link": reset_link
            }

            # Send the email notification
            if not send_email_notification("recoveryPassword", email_data):
                log_audit(
                    user = user.get("name", "Usuario"),
                    action_type = AuditActionType.USER_PASSWORD_RESET,
                    details = "Fallo al enviar el correo de recuperación de contraseña",
                )
                flash("Error al enviar correo, por favor, intenta de nuevo.", "danger")
                return redirect(url_for("recoveryPassword.recoveryPasswordView"))
            
            log_audit(
                user = user.get("name", "Usuario"),
                action_type = AuditActionType.USER_PASSWORD_RESET,
                details = "Correo de recuperación de contraseña enviado",
                )
            
            flash("Correo de recuperación enviado correctamente, por favor revisa tu correo.", "success")
            return redirect(url_for("recoveryPassword.recoveryPasswordView"))
        else:
            flash("Ingrese una dirección de correo válida.", "danger")
            return redirect(url_for("recoveryPassword.recoveryPasswordView"))
    else:
        flash("Please enter a valid email address.", "danger")

    return redirect(url_for("recoveryPassword.recoveryPasswordView"))

def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps(email, salt='password-recovery-salt')

@rec_password_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password_form(token):
    serializer = URLSafeTimedSerializer(current_app.secret_key)

    try:
        email = serializer.loads(token, salt='password-recovery-salt', max_age=900)  # 15 minutos
    except Exception:
        flash("Token invalido o expiró", "danger")
        return redirect(url_for("recoveryPassword.recoveryPasswordView"))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if new_password != confirm_password:
            flash("Las contraseñas no coinciden.", "danger")
            return redirect(url_for("recoveryPassword.reset_password_form", token=token))
        
        # Actualizar la contraseña en Firebase
        repo.update_user_password(email, new_password)
        
        flash("Contraseña actualizada correctamente.", "success")
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", token=token)
