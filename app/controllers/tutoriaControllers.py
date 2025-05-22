from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..models.repositories.tutorings.repoTutorials import RepoTutoring
# from ..models.repositories.tutorings.firebase_tutorings_repository import FirebaseTutoringRepository
from app.utils.auth import login_required

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

@tutoring.route('/tutorial/list')
def getListTutorials():
    tutorials = repo.list_tutorials()
    if tutorials is None:
        print("Tutoring not found")
        return render_template('404.html'), 404
    else:
        return render_template('list_tutorials.html', tutorias=tutorials, len=len)

@tutoring.route('/tutorial/register_tutoria', methods=["POST"])
@login_required
def register_tutoria():
    id_tutoria = request.form["id_tutoria"]
    id_student = session["user_id"]  # Obtener el ID del usuario autenticado desde la sesión
    name_student = session.get("user_name", "Usuario Anónimo")  # Obtener el nombre del usuario autenticado

    tutoria = repo.get_tutoria_by_id(id_tutoria)
    if tutoria:
        if tutoria.capacity == len(tutoria.student_list):
            flash("No hay cupos disponibles para esta tutoría.", "warning")
        elif any(student["id"] == id_student for student in tutoria.student_list):
            flash("Ya estás registrado en esta tutoría.", "info")
        else:
            exito = repo.register_in_tutoria(id_student, name_student, id_tutoria)
            if exito:
                flash("Te has registrado exitosamente.", "success")
                tutoria.capacity -= 1
            else:
                flash("No fue posible registrarte.", "danger")
    else:
        flash("La tutoría no fue encontrada.", "danger")

    return redirect(url_for('tutorial.getListTutorials'))


