from flask import Blueprint, render_template, request, jsonify
# from flask_login import login_required
from functools import wraps
# from app.models.user import User
# from app.models.tutorial import Tutorial
# from app.models.review import Review
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

user_repo = FirebaseUserRepository()
from app.models.services.email_service import SMTPEmailService


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # TODO: Implement admin check logic
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/')
@admin_required
def dashboard():
  return render_template('admin/dashboard.html')

# @admin_bp.route('/users')
# @admin_required
# @app.route('/admin/users')

@admin_bp.route('/users', methods=['GET', 'POST'])
@admin_required
def users():
    if request.method == 'POST':
        # This is the AJAX request to update user status:
        try:
            data = request.get_json(force=True)
            email = data.get('email')
            status = data.get('status')

            if email is None or status is None:
                return jsonify({"success": False, "error": "Missing parameters"}), 400

            status_bool = bool(status)
            success = user_repo.update_user_status(email, status_bool)

            if success:
                return jsonify({"success": True})
            else:
                return jsonify({"success": False, "error": "Failed to update status"}), 500

        except Exception as e:
            print(f"Error updating status: {e}")
            return jsonify({"success": False, "error": str(e)}), 500

    else:
        # This is the GET request to render the users page:
        users = user_repo.get_all_users()
        return render_template('admin/users.html', users=users)


@admin_bp.route('/tutorials')
@admin_required
def tutorials():
    return "<h1>Tutorials</h1>"

@admin_bp.route('/reviews')
@admin_required
def reviews():
    return "<h1>Reviews</h1>"

@admin_bp.route('/logs')
@admin_required
def logs():
    return "<h1>Logs</h1>"

@admin_bp.route('/settings')
@admin_required
def settings():
    return "<h1>Settings</h1>"


@admin_bp.route('/send-ban-email', methods=['POST'])
@admin_required
def ban_notification_emai():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify(success=False, error='Email no proporcionado')
    subject = "Banneo temporal"
    message = "Usted ha incumplido las reglas de este servicio, por lo tanto será baneado"
    SendBanEmail = SMTPEmailService()
    success = SendBanEmail.send_email(email,subject,message)
    if(success):
     return jsonify(success=True, message='Usuario notificado con éxito')
    else:
     return jsonify(success=True, message='Usuario notificado con éxito')

    
