from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from app.models.services import email_notifier
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
# Para crear token firmado
from itsdangerous import URLSafeTimedSerializer
# Para enviar correo

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
            flash("Recovery email sent successfully.", "success")
            return render_template("recovery_pass_token.html")
        else:
            flash("Please enter a valid email address.", "danger")
            return redirect(url_for("recoveryPassword.recoveryPasswordView"))
    else:
        flash("Please enter a valid email address.", "danger")

    return redirect(url_for("recoveryPassword.recoveryPasswordView"))

def generate_password_reset_token(email):
    serializer = URLSafeTimedSerializer(current_app.config['secret_key'])
    return serializer.dumps(email, salt='password-recovery-salt')

@rec_password_bp.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_password_form(token):
    serializer = URLSafeTimedSerializer(current_app.config['secret_key'])

    try:
        email = serializer.loads(token, salt='password-recovery-salt', max_age=900)  # 15 minutos
    except Exception:
        flash("Token invalido o expiró", "danger")
        return redirect(url_for("recoveryPassword.recoveryPasswordView"))

    if request.method == 'POST':
        new_password = request.form.get('password')
        FirebaseUserRepository.update_user_password(email, new_password)
        flash("Password reset successfully.", "success")
        return redirect(url_for("login"))

    return render_template("reset_password.html", token=token)
