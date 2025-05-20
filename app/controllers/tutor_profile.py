from flask import Blueprint, render_template, session, redirect, url_for
from ..utils.auth import login_and_role_required
from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository

tutor_bp = Blueprint('tutor', __name__)
repo = FirebaseTutoringRepository()

@tutor_bp.route('/profile')
@login_and_role_required ('Tutor')
def tutor_profile():
  if session.get('role') != 'Tutor':
    return redirect(url_for('home.home'))
  
  tutor_id = session.get('user_id')
  tutorias = repo.get_tutorias_by_tutor(tutor_id)
  return render_template('tutor_profile.html', tutorias=tutorias)