from flask import Flask

from .extensions import mail
import os

app = Flask(__name__)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL PORT'] = 465
app.config['MAIL USERNAME'] = os.getenv('DEL_EMAIL')
app.config['MAIL PASSWORD'] = os.getenv('PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = True

mail.init_app(app)

from .controllers.home import home as home_blueprint
from .controllers.mail_sender import mail as mail_sender_blueprint

# Register blueprints
app.register_blueprint(home_blueprint)
app.register_blueprint(mail_sender_blueprint)
