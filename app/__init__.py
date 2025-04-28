from flask import Flask


app = Flask(__name__)

from .controllers.home import home as home_blueprint
from .controllers.tutoriaControllers import tutoring as tutoria_blueprint

# Register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(tutoria_blueprint)
