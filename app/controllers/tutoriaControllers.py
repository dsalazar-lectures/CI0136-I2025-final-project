from flask import Blueprint, render_template
from ..models.repoTutorias import RepoTutorias

tutoria = Blueprint('tutoria', __name__)

repo = RepoTutorias()

@tutoria.route('/tutoria/<id>')

def getTutoriaById(id):
    tutoria = repo.get_tutoria_by_id(id)

    if tutoria is None:
        return render_template('404.html'), 404
    else:
        return render_template('tutoria.html', tutoria=tutoria, estudiantes=tutoria.estudiantes_inscritos)