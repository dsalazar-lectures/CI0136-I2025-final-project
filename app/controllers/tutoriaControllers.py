from flask import Blueprint, render_template
from ..models.repoTutorias import RepoTutoring

tutoring = Blueprint('tutoring', __name__)

repo = RepoTutoring()

@tutoring.route('/tutoring/<id>')

def getTutoriaById(id):
    tutoring = repo.get_tutoria_by_id(id)

    if tutoring is None:
        return render_template('404.html'), 404
    else:
        return render_template('tutoria.html', tutoring=tutoring)