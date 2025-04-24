from flask import Flask
"""
This module initializes the Flask application and registers the blueprints for it.
Modules:
"""

app = Flask(__name__)

from .controllers.home import home as home_blueprint
from .controllers.register import register_bp as register_blueprint  

# home_blueprint: Blueprint for handling routes related to the home page.
app.register_blueprint(home_blueprint)
# register_blueprint: Blueprint for handling routes related to user registration.
app.register_blueprint(register_blueprint)
