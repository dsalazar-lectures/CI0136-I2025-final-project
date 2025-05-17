from flask import Blueprint, render_template
#from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository

tutoring = Blueprint('tutoring', __name__)

#repo = FirebaseTutoringRepository()

@tutoring.route('/tutoring/<id>')

def getTutoriaById(id):
    tutoring = repo.get_tutoria_by_id(id)

    if tutoring is None:
        print("Tutoring not found")
        return render_template('404.html'), 404
    else:
        return render_template('tutoria.html', tutoring=tutoring)