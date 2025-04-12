from flask import Blueprint, render_template

home = Blueprint('home', __name__)

@home.route("/")
@home.route('/<name>')
def greeting(name=None):
    return render_template('home.html', person=name)