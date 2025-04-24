from flask import Blueprint, render_template
from ..services.tutoriaServices import getTutoriaByID

tutoria = Blueprint('tutoria', __name__)

@tutoria.route('/tutoria/<id>')

def getTutoriaById(id):
    tutoria = getTutoriaByID()
    for t in tutoria:
        if t.id == int(id):
            return render_template('tutoria.html', tutoria=t)
    return render_template('404.html'), 404