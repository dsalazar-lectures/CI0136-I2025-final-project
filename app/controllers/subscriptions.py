from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.auth import login_or_role_required
from ..models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository

subscriptions_bp = Blueprint('subscriptions', __name__)
repo = FirebaseTutoringRepository()

@subscriptions_bp.route('/')
@login_or_role_required('Student')
def get_subscriptions():
    if session.get('role') != 'Student':
        return redirect(url_for('home.home'))
    
    student_id = session.get('user_id')
    print(f"Student ID: {student_id}")
    tutorias = repo.get_tutorias_by_student(student_id)
    print(f"Student Tutorias: {tutorias}")
    return render_template('subscriptions.html', tutorias=tutorias)