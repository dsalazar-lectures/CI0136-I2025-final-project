from flask import Blueprint, render_template, request, redirect, url_for
from ..models.repositories.tutorings.repoTutorials import RepoTutoring
# from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository

tutoring = Blueprint('tutorial', __name__)

repo = RepoTutoring()

@tutoring.route('/tutorial/<id>')

def getTutoriaById(id):
    tutoring = repo.get_tutoria_by_id(id)

    if tutoring is None:
        print("Tutorial not found")
        return render_template('404.html'), 404
    else:
        return render_template('tutorial.html', tutoring=tutoring)
    
@tutoring.route('/tutorial/create', methods=['GET', 'POST'])
def create_tutoring():
    if request.method == 'POST':
        title_tutoring = request.form['title_tutoring']
        tutor_id = int(request.form['tutor_id'])
        subject = request.form['subject']
        date = request.form['date']
        start_time = request.form['start_time']
        description = request.form['description']
        method = request.form['method']
        capacity = int(request.form['capacity'])

        new_tutoring = repo.create_tutoria(
            title_tutoring, tutor_id, subject, date, start_time, description, method, capacity
        )
        return redirect(url_for('tutorial.getTutoriaById', id=new_tutoring.id))
    return render_template('tutorial_creation.html')