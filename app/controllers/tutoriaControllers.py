from flask import Blueprint, render_template
from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository
from ..utils.auth import login_or_role_required

tutoring = Blueprint('tutoring', __name__)

repo = FirebaseTutoringRepository()

@tutoring.route('/tutoring/<id>')
@login_or_role_required ('Tutor')
def getTutoriaById(id):
    tutoring = repo.get_tutoria_by_id(id)

    if tutoring is None:
        print("Tutoring not found")
        return render_template('404.html'), 404
    else:
        return render_template('tutoria.html', tutoring=tutoring)