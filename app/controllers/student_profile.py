from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.auth import login_required
from ..models.repositories.tutorings.repoTutorials import RepoTutoring

student_bp = Blueprint('student', __name__)
repo = RepoTutoring()

@student_bp.route('/profile')
@login_required
def student_profile():
    if session.get('role') != 'Student':
        return redirect(url_for('home.home'))
    
    student_id = session.get('user_id')
    tutorias = repo.get_tutorias_by_student(student_id)
    return render_template('student_profile.html', tutorias=tutorias)