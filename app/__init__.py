from flask import Flask
from app.models.Note import db
from app.middleware.error_logging import error_logging_middleware


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize error logging middleware
error_logging_middleware(app)

from .controllers.home import home as home_blueprint
from .controllers.notes import notes as notes_blueprint

db.init_app(app)

# Register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(notes_blueprint)

with app.app_context():
    db.create_all() 
