"""
Flask application initialization.
This file creates the Flask app instance and registers all blueprints.
"""
from flask import Flask
from app.middleware.error_logging import error_logging_middleware

app = Flask(__name__)
# Initialize error logging middleware
error_logging_middleware(app)
# Secret key for session management and CSRF(Cross Site Request Forgery) protection
app.secret_key = 'some-secret'

# Import blueprint modules
from .controllers.home import home_bp as home_blueprint
from .controllers.register import register_bp as register_blueprint  
from .controllers.auth import auth_bp as auth_blueprint
from .controllers.tutoriaControllers import tutoring as tutoria_blueprint
from .controllers.comments import comments_bp
from .controllers.ratings import ratings_bp
from .routes.email_routes import mail_bp

   # Register blueprints to enable routing
app.register_blueprint(home_blueprint)          # Home page routes
app.register_blueprint(register_blueprint)      # Registration routes
app.register_blueprint(auth_blueprint)          # Authentication routes
app.register_blueprint(tutoria_blueprint)      # Tutoring routes
app.register_blueprint(comments_bp)
app.register_blueprint(ratings_bp, url_prefix='/comments')
app.register_blueprint(mail_bp, purl_prefix='/email')
