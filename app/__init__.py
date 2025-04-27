from flask import Flask

app = Flask(__name__)
app.secret_key = 'some-secret'

from .controllers.home import home_bp as home_blueprint
from .controllers.register import register_bp as register_blueprint  
from .controllers.auth import auth_bp as auth_blueprint

# home page routes
app.register_blueprint(home_blueprint)
# registration routes
app.register_blueprint(register_blueprint)
# authentication routes
app.register_blueprint(auth_blueprint)