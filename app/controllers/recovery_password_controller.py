from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.services import email_notifier
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
# Para crear token firmado
from itsdangerous import URLSafeTimedSerializer
# Para enviar correo
from app.services.notification import send_email_notification
# Para logs
from app.services.audit import log_audit, AuditActionType

from app.utils.utils import validate_password

repo = FirebaseUserRepository()

rec_password_bp = Blueprint('recoveryPassword', __name__)

@rec_password_bp.route("/recovery_password", methods=['GET'])
def recoveryPasswordView(): 
    return render_template("recovery_password.html")

@rec_password_bp.route("/recovery_password", methods=['POST'])
def recover():
    """
    Handle password recovery requests.
    Validates the email address, generates a password reset token,
    and sends a recovery email to the user.
    """
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
                    details = "Failed to send recovery email",
                )
                flash("Failed to send recovery email. Please try again later.", "danger")
                return redirect(url_for("recoveryPassword.recoveryPasswordView"))
            
            flash("If email exists, recovery email sent successfully. Please check your inbox.", "success")
            log_audit(
                user = user.get("name", "Usuario"),
                action_type = AuditActionType.USER_PASSWORD_RESET,
                details = "Password recovery email sent",
            )
            return redirect(url_for("recoveryPassword.recoveryPasswordView"))
        else:
            flash("If email exists, recovery email sent successfully. Please check your inbox.", "success")
            log_audit(
                user= userEmail,
                action_type = AuditActionType.USER_PASSWORD_RESET,
                details = "Attempted password recovery with invalid email",
            )
            return redirect(url_for("recoveryPassword.recoveryPasswordView"))
    else:
        flash("Please enter a valid email address.", "danger")

    return redirect(url_for("recoveryPassword.recoveryPasswordView"))

def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.secret_key)
    return serializer.dumps(email, salt='password-recovery-salt')

@rec_password_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password_form(token):
    """
    Handle the password reset form submission.
    Validates the token, checks if the new password meets criteria, and updates the password in the database.
    """
    serializer = URLSafeTimedSerializer(current_app.secret_key)

    try:
        email = serializer.loads(token, salt='password-recovery-salt', max_age=900)  # 15 minutos
    except Exception:
        flash("Invalid or expired token", "danger")
        return redirect(url_for("recoveryPassword.recoveryPasswordView"))

    if request.method == 'POST':
        new_password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        error_message, error_category = validate_new_password(new_password, confirm_password)
        if error_message:
            flash(error_message, error_category)
            return redirect(url_for("recoveryPassword.reset_password_form", token=token))
        
        # Actualizar la contraseña en Firebase
        repo.update_user_password(email, new_password)
        user = repo.get_user_by_email(email)
        
        flash("Password updated successfully", "success")
        log_audit(
            user = user.get("name", "Usuario"),
            action_type = AuditActionType.USER_PASSWORD_RESET,
            details = "Password updated successfully",
        )

        # Enviar correo de confirmación
        email_data = {
            "username": user.get("name", "Usuario"),
            "emailTo": email,
        }
        if not send_email_notification("successPasswordChange", email_data):
            log_audit(
                user = user.get("name", "Usuario"),
                action_type = AuditActionType.USER_PASSWORD_RESET,
                details = "Failed to send confirmation email",
            )
            return redirect(url_for("recoveryPassword.reset_password_form", token=token))
        
        return redirect(url_for("auth.login"))

    return render_template("reset_password.html", token=token)

def validate_new_password(new_password, confirm_password):
    """
    Validates the new password and its confirmation.
    
    Args:
        * new_password (str): The new password entered by the user.
        * confirm_password (str): The confirmation password entered by the user.
    
    Returns:
        * error_message (str): Error message if validation fails, None otherwise.
        * error_category (str): Category of the error ('danger') if validation fails, None otherwise.
    """

    if len(new_password) < 8:
        return "Password must be at least 8 characters long", "danger"
    if not validate_password(new_password):
        return "Password must include at least one uppercase letter, one number, and one special character", "danger"
    if new_password != confirm_password:
        return "Passwords do not match", "danger"
    return None, None