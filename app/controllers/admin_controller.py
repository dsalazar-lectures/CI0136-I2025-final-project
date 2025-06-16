from app.models.repositories.firebase_log_repository import FirebaseLogRepository
from app.services.audit.log_querying_service import LogQueryingService
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from ..utils.auth import login_or_role_required
from app.services.admin.admin_metrics_service import get_admin_metrics

# from flask_login import login_required
from functools import wraps
# from app.models.user import User
# from app.models.tutorial import Tutorial
# from app.models.review import Review
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

user_repo = FirebaseUserRepository()
from app.services.ban_notification_service.ban_notification_types import *


@admin_bp.route('/')
@login_or_role_required('Admin')
def dashboard():
    metrics = get_admin_metrics()
    return render_template('admin/dashboard.html', metrics=metrics)

# @admin_bp.route('/users')
# @admin_required
# @app.route('/admin/users')

@admin_bp.route('/users', methods=['GET', 'POST'])
@login_or_role_required('Admin')
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
@login_or_role_required('Admin')
def tutorials():
    return "<h1>Tutorials</h1>"

@admin_bp.route('/reviews')
@login_or_role_required('Admin')
def reviews():
    return "<h1>Reviews</h1>"


@admin_bp.route('/settings')
@login_or_role_required('Admin')
def settings():
    return "<h1>Settings</h1>"

@admin_bp.route('/logs')
@login_or_role_required('Admin')
def logs_redirect():
    LOGS_PER_PAGE = 10
    return redirect(url_for('admin.logs', page_number=0, logs_per_page=LOGS_PER_PAGE))

@admin_bp.route('/logs/page_number=<page_number>&logs_per_page=<logs_per_page>')
@login_or_role_required('Admin')
def logs(page_number, logs_per_page):
    page_number = int(page_number)
    logs_per_page = int(logs_per_page)
    log_service = LogQueryingService(FirebaseLogRepository())
    logs = log_service.get_log_page(page_number, logs_per_page)
    log_count = int(log_service.get_log_count())
    return render_template("admin/log_list.html", logs=logs, log_count=log_count)

@admin_bp.route('/send-ban-email', methods=['POST'])
@login_or_role_required('Admin')
def ban_notification_emai():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify(success=False, error='Email no proporcionado')
    type = "behavior"
    notification = BanNotificationFactory.create_ban_notification(type)
    notification.notify(email)
    if(True):
     return jsonify(success=True, message='Usuario notificado con éxito')
    else:
     return jsonify(success=True, message='Usuario notificado con éxito')


