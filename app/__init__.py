"""
Flask application initialization.
This file creates the Flask app instance and registers all blueprints.
"""
from flask import Flask, render_template
from app.middleware.error_logging import error_logging_middleware
from app.firebase_config import initialize_firebase

app = Flask(__name__)
# Initialize error logging middleware
error_logging_middleware(app)
# Secret key for session management and CSRF(Cross Site Request Forgery) protection
app.secret_key = 'some-secret'

# # Inicializar Firebase
initialize_firebase()

# Import blueprint modules
from .controllers.home import home_bp as home_blueprint
from .controllers.register import register_bp as register_blueprint  
from .controllers.auth import auth_bp as auth_blueprint
from .controllers.tutoriaControllers import tutoring as tutoria_blueprint
from .controllers.comments import comments_bp
from .controllers.ratings import ratings_bp
from .controllers.email_controller import mail_bp
from .controllers.profile_controller import profile_bp as profile_blueprint

# Register blueprints to enable routing
app.register_blueprint(home_blueprint)          # Home page routes
app.register_blueprint(register_blueprint)      # Registration routes
app.register_blueprint(auth_blueprint)          # Authentication routes
app.register_blueprint(tutoria_blueprint)      # Tutoring routes
app.register_blueprint(comments_bp)
app.register_blueprint(ratings_bp, url_prefix='/comments')
app.register_blueprint(mail_bp, url_prefix='/email')
app.register_blueprint(profile_blueprint, url_prefix='/profile')