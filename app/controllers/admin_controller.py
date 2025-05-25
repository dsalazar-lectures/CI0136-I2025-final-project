from app.models.repositories.firebase_log_repository import FirebaseLogRepository
from app.services.audit.log_querying_service import LogQueryingService
from flask import Blueprint, render_template
# from flask_login import login_required
from functools import wraps
# from app.models.user import User
# from app.models.tutorial import Tutorial
# from app.models.review import Review

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

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

@admin_bp.route('/users')
@admin_required
def users():
    return "<h1>Users</h1>"

@admin_bp.route('/tutorials')
@admin_required
def tutorials():
    return "<h1>Tutorials</h1>"

@admin_bp.route('/reviews')
@admin_required
def reviews():
    return "<h1>Reviews</h1>"

@admin_bp.route('/settings')
@admin_required
def settings():
    return "<h1>Settings</h1>"

@admin_bp.route('/logs/page_number=<page_number>&logs_per_page=<logs_per_page>')
@admin_required
def logs(page_number, logs_per_page):
    logs = LogQueryingService(FirebaseLogRepository()).get_log_page(int(page_number), int(logs_per_page))
    return render_template("log_list.html", logs = logs)