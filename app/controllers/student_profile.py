from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.auth import login_or_role_required
from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository

student_bp = Blueprint('student', __name__)
repo = FirebaseTutoringRepository()

@student_bp.route('/profile')
@login_or_role_required('Student')
def student_profile():
    if session.get('role') != 'Student':
        return redirect(url_for('home.home'))
    
    student_id = session.get('user_id')
    print(f"Student ID: {student_id}")
    tutorias = repo.get_tutorias_by_student(student_id)
    print(f"Student Tutorias: {tutorias}")
    return render_template('student_profile.html', tutorias=tutorias)