from flask import Flask


app = Flask(__name__)

from .controllers.home import home as home_blueprint

# Register blueprints
app.register_blueprint(home_blueprint)
