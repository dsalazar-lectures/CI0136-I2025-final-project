from flask import Blueprint, render_template, redirect, url_for
from app.models.services.email_service import send_login_notification
import os

mail = Blueprint('mail', __name__)

@mail.route('/mail')
def greeting(name=None):
    return render_template('sendmailbtn.html', person=name)


@mail.route('/send-test-email', methods=['POST'])
def send_test_email():
    send_login_notification(os.getenv('REC_EMAIL'))
    return redirect(url_for('mail.greeting'))