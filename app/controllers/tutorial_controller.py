from flask import Blueprint, render_template, request, redirect, url_for
from ..models.repositories.tutorial.repoTutorials import Tutorial_mock_repo
# from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository

tutorial = Blueprint('tutorial', __name__)

repo = Tutorial_mock_repo()

@tutorial.route('/tutorial/<id>')

def getTutoriaById(id):
    tutoring = repo.get_tutorial_by_id(id)

    if tutoring is None:
        print("Tutorial not found")
        return render_template('404.html'), 404
    else:
        return render_template('tutorial.html', tutoring=tutoring)
    
@tutorial.route('/tutorial/create', methods=['GET', 'POST'])
def create_tutorial():
    if request.method == 'POST':
        title_tutoring = request.form['title_tutoring']
        subject = request.form['subject']
        date = request.form['date']
        start_time = request.form['start_time']
        description = request.form['description']
        method = request.form['method']
        capacity = int(request.form['capacity'])

        tutor_id = 2 # This should be replaced with the actual tutor ID from DB
        tutor = "Ana Gómez" # This should be replaced with the actual tutor name from the DB

        #TODO: Get the tutor ID and name from DB

        new_tutorial = repo.create_tutorial(
            title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity
        )
        return redirect(url_for('tutorial.getTutoriaById', id=new_tutorial.id))
    return render_template('tutorial_creation.html')