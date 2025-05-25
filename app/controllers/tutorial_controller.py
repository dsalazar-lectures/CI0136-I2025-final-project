from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..models.repositories.tutorial.repoTutorials import Tutorial_mock_repo
from ..models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from ..utils.auth import login_or_role_required
#from flask_login import login_required
tutorial = Blueprint('tutorial', __name__)

repo = Tutorial_mock_repo()
repo1 = FirebaseTutoringRepository()

@tutorial.route('/tutorial/<id>')

def getTutoriaById(id):
    tutoring = repo.get_tutorial_by_id(id)
    #tutoring = repo1.get_tutoria_by_id(id)  # Cambié el repositorio mock por el repositorio de Firebase
    user_role = request.args.get('user_role', 'student')
    if tutoring is None:
        print("Tutorial not found")
        return render_template('404.html'), 404
    else:
        return render_template('tutorial.html',tutoring=tutoring, user_role=user_role)
    
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
        return redirect(url_for('tutorial.listTutorTutorials'))
    return render_template('tutorial_form.html', tutoring=None, edit_mode=False)

@tutorial.route('/tutorial/<id>/edit', methods=['GET', 'POST'])
def edit_tutorial(id):
    tutoring = repo.get_tutorial_by_id(id)

    if tutoring is None:
        return render_template('404.html'), 404

    if request.method == 'POST':
        updated_data = {
            'title_tutoring': request.form['title_tutoring'],
            'subject': request.form['subject'],
            'date': request.form['date'],
            'start_time': request.form['start_time'],
            'description': request.form['description'],
            'method': request.form['method'],
            'capacity': int(request.form['capacity']),
        }

        repo.update_tutorial(id, updated_data)
        return redirect(url_for('tutorial.listTutorTutorials'))

    return render_template('tutorial_form.html', tutoring=tutoring, edit_mode=True)


@tutorial.route('/tutorial/list')
def getListTutorials():
    #tutorials = repo1.get_list_tutorials()
    tutorials = repo.list_tutorials()
    print("TUTORIAS:", tutorials) 
    if tutorials is None:
        print("Tutoring not found")
        return render_template('404.html'), 404
    else:
        return render_template('list_tutorials.html', tutorias=tutorials, len=len)

@tutorial.route('/tutorial/register_tutoria', methods=["POST"])
@login_or_role_required ('Student')
def register_tutoria():
    print(session)
    id_tutoria = request.form["id_tutoria"]
    id_student = session.get('user_id')
    name_student = session.get("name", "usuario anonimo")  # Obtener el nombre del usuario autenticado
    print(f"ID del estudiante: {id_student}")
    print(name_student)
    #tutoria = repo1.get_tutoria_by_id(id_tutoria)
    tutoria = repo.get_tutorial_by_id(id_tutoria) 
    if tutoria:
        if tutoria.capacity == len(tutoria.student_list):
            flash("No hay cupos disponibles para esta tutoría.", "warning")
        elif any(student["id"] == id_student for student in tutoria.student_list):
            flash("Ya estás registrado en esta tutoría.", "info")
        else:
            #exito = repo1.register_in_tutoria(id_student, name_student, id_tutoria)
            exito = repo.register_in_tutoria(id_student, name_student, id_tutoria)  # Cambié el repositorio mock por el repositorio de Firebase
            if exito:
                flash("Te has registrado exitosamente.", "success")
                tutoria.capacity -= 1
            else:
                flash("No fue posible registrarte.", "danger")
    else:
        flash("La tutoría no fue encontrada.", "danger")

    return redirect(url_for('tutorial.getListTutorials'))


@tutorial.route('/tutorial/tutor_tutorials')
@login_or_role_required('Tutor')
def listTutorTutorials():
    tutor_id = 2
    if not tutor_id:
        flash("No se pudo obtener el ID del tutor.", "danger")
        return redirect(url_for('tutorial.getListTutorials'))

    search = request.args.get('search', '').lower()
    sort = request.args.get('sort')

    tutorias = repo.get_tutorias_by_tutor(tutor_id)

    if search:
        tutorias = [
            t for t in tutorias if search in t.title.lower() or search in t.subject.lower()
        ]

    if sort == 'asc':
        tutorias.sort(key=lambda t: t.date)
    elif sort == 'desc':
        tutorias.sort(key=lambda t: t.date, reverse=True)

    return render_template('tutor_tutorials.html', tutorias=tutorias)
