from flask import Flask
from app.models.Note import db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///notes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



from .controllers.home import home as home_blueprint
from .controllers.notes import notes as notes_blueprint

db.init_app(app)

# Register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(notes_blueprint)

with app.app_context():
    db.create_all() 
