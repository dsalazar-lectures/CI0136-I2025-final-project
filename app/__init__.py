from flask import Flask
from app.middleware.error_logging import error_logging_middleware


app = Flask(__name__)
# Initialize error logging middleware
error_logging_middleware(app)

from .controllers.home import home as home_blueprint

# Register blueprints
app.register_blueprint(home_blueprint)
