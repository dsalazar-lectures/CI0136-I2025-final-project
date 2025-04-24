from flask import Blueprint, render_template
from app.services.audit import log_audit, AuditActionType
home = Blueprint('home', __name__)

@home.route("/")
@home.route('/<name>')
def greeting(name=None):
    log_audit("Aaron", AuditActionType.CONTENT_READ, "Home page viewed")
    return render_template('home.html', person=name)