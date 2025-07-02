"""
Flask application initialization.
This file creates the Flask app instance and registers all blueprints.
"""
from flask import Flask, render_template, session, request, redirect, url_for
from app.middleware.error_logging import error_logging_middleware
from app.firebase_config import initialize_firebase
from app.utils.error_handlers import register_error_handlers


app = Flask(__name__)
# Initialize error logging middleware
error_logging_middleware(app)
# Secret key for session management and CSRF(Cross Site Request Forgery) protection
app.secret_key = 'some-secret'

initialize_firebase()
register_error_handlers(app)


@app.before_request
def clear_session_on_restart():
    if request.endpoint == "auth.login" and request.method == "GET" and "user_id" in session:
        session.clear()


# Import blueprint modules
from .controllers.home import home_bp as home_blueprint
from .controllers.register import register_bp as register_blueprint
from .controllers.auth import auth_bp as auth_blueprint
from .controllers.tutorial_controller import tutorial as tutorial_blueprint
from .controllers.comments import comments_bp
from .controllers.ratings import ratings_bp
from .controllers.subscriptions import subscriptions_bp
from .routes.review_routes import review_bp
from .controllers.profile_controller import profile_bp as profile_blueprint
from .controllers.admin_controller import admin_bp as admin_blueprint
from .controllers.change_password_controller import c_password_bp as change_pass
from .controllers.recovery_password_controller import rec_password_bp as recovery_pass
from.controllers.user_preferences_controller import userPreferencesSetting as preferencesSettings
from .routes.simple_media_routes import simple_media_bp

# redirect / to /home
@app.route('/')
def redirect_to_home():
    return redirect(url_for('home.home'))


# Register blueprints to enable routing
app.register_blueprint(review_bp)
app.register_blueprint(home_blueprint)          # Home page routes
app.register_blueprint(register_blueprint)      # Registration routes
app.register_blueprint(auth_blueprint)          # Authentication routes
app.register_blueprint(tutorial_blueprint)      # Tutoring routes
app.register_blueprint(comments_bp)
app.register_blueprint(ratings_bp, url_prefix='/comments')
app.register_blueprint(profile_blueprint, url_prefix="/profile")
app.register_blueprint(admin_blueprint)         # Admin routes
app.register_blueprint(subscriptions_bp, url_prefix='/subscriptions')  # Student profile routes
app.register_blueprint(change_pass)
app.register_blueprint(recovery_pass)
app.register_blueprint(preferencesSettings)
app.register_blueprint(simple_media_bp)

