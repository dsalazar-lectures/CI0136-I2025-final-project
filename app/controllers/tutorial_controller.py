from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from ..models.repositories.tutorial.repoTutorials import Tutorial_mock_repo
from ..models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository
from ..models.builders.button_factory.button_factory import button_factory
from ..utils.auth import login_or_role_required
from app.services.notification import send_email_notification
from app.services.audit import log_audit, AuditActionType
from app.utils.date_utils import get_current_datetime
from datetime import datetime
#from flask_login import login_required
tutorial = Blueprint('tutorial', __name__)

repo = Tutorial_mock_repo()
firebase_repo = FirebaseTutoringRepository()

@tutorial.route('/tutorial/<id>')

def getTutoriaById(id):

    # tutoring = repo.get_tutorial_by_id(id)
    tutoring = firebase_repo.get_tutorial_by_id(id)  # Cambié el repositorio mock por el repositorio de Firebase
    
    user_role = request.args.get('user_role', 'student')
    current_user = session.get("name", "usuario anonimo") 

    if (
         user_role == "student" and
        tutoring.student_list and
        any(student.get("name") == current_user for student in tutoring.student_list) and
        -20 < measure_time_to_tutorial(id) <= 30
    ):
        factory = button_factory("zoom")
        button = factory.create_button(tutoring.meeting_link)
    else:
        button = None
    
    if tutoring is None:
        print("Tutorial not found")
        return render_template('404.html'), 404
    else:
        return render_template('tutorial.html',tutoring=tutoring, user_role=user_role, button=button)
    
@tutorial.route('/tutorial/create', methods=['GET', 'POST'])
@login_or_role_required('Tutor')
def create_tutorial():
    if request.method == 'POST':
        title_tutoring = request.form['title_tutoring']
        subject = request.form['subject']
        date = request.form['date']
        start_time = request.form['start_time']
        description = request.form['description']
        method = request.form['method']
        capacity = int(request.form['capacity'])
        is_virtual = method.lower() == 'virtual'  # Variable booleana para determinar si es virtual
        meeting_link = request.form['meeting_link'] if is_virtual else None
        tutor_id = session.get('user_id')
        tutor = session.get('name', 'Tutor Anónimo')  # Default to 'Tutor Anónimo' if name is not set

        # tutor_id = 2
        # tutor = "Ana Gómez"

        new_tutorial = firebase_repo.create_tutorial(
            title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity, meeting_link
        )
        if new_tutorial:
            # Send a notification email
            email_data = {
                "username": tutor,
                "emailTo": session.get("email", "tutorialsflaskmail@gmail.com"),
                "tutorial": title_tutoring,
            }
            if not send_email_notification("newTutorial", email_data):
                log_audit(
                    user = tutor,
                    action_type=AuditActionType.CONTENT_CREATE,
                    details = "Failed to send email notification for new tutorial creation: " + title_tutoring,
                )
            flash("Tutoría creada exitosamente.", "success")
        else:
            flash("Error al crear la tutoría. Por favor, inténtalo de nuevo.", "danger")
        return redirect(url_for('tutorial.listTutorTutorials'))
    return render_template('tutorial_form.html', tutoring=None, edit_mode=False)

@tutorial.route('/tutorial/<id>/edit', methods=['GET', 'POST'])
@login_or_role_required('Tutor')
def edit_tutorial(id):
    tutoring = firebase_repo.get_tutorial_by_id(id)

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
            'meeting_link': request.form['meeting_link'] 
        }
            # Agregar solo si es virtual
        

        firebase_repo.update_tutorial(id, updated_data)
        return redirect(url_for('tutorial.listTutorTutorials'))

    return render_template('tutorial_form.html', tutoring=tutoring, edit_mode=True)


@tutorial.route('/tutorial/list')
def getListTutorials():
    tutorials = firebase_repo.get_list_tutorials()
    #tutorials = repo.list_tutorials()
    print("TUTORIAS:", tutorials) 
    if tutorials is None:
        print("Tutoring not found")
        return render_template('404.html'), 404
    else:
        search = request.args.get('search', '').lower()
        sort = request.args.get('sort')
        subject_filter = request.args.get('subject')

        all_subjects = sorted(list(set(t.subject for t in tutorials if hasattr(t, 'subject'))))
        if search:
            tutorials = [
                t for t in tutorials
                if search in t.title.lower()
                or search in t.subject.lower()
                or search in t.description.lower()
            ]
        if subject_filter:
            tutorials = [t for t in tutorials if t.subject == subject_filter]

        if sort == "asc":
            tutorials.sort(key=lambda t: t.date)
        elif sort == "desc":
            tutorials.sort(key=lambda t: t.date, reverse=True)

        return render_template(
            'list_tutorials.html',
            tutorias=tutorials,
            len=len,
            all_subjects=all_subjects,
            current_subject=subject_filter,
            current_sort=sort,
            current_search=search
        )

@tutorial.route('/tutorial/register_tutoria', methods=["POST"])
@login_or_role_required ('Student')
def register_tutoria():
    print(session)
    id_tutoria = request.form["id_tutoria"]
    id_student = session.get('user_id')
    name_student = session.get("name", "usuario anonimo") 
    print(f"ID del estudiante: {id_student}")
    print(name_student)
    tutoria = firebase_repo.get_tutorial_by_id(id_tutoria)
    #tutoria = repo.get_tutorial_by_id(id_tutoria) 
    if tutoria:
        if tutoria.capacity == len(tutoria.student_list):
            flash("No hay cupos disponibles para esta tutoría.", "warning")
        elif any(str(student["id"]) == str(id_student) for student in tutoria.student_list):
            flash("Ya estás registrado en esta tutoría.", "info")
        else:
            exito = firebase_repo.register_in_tutoria(id_student, name_student, id_tutoria)
            #exito = repo.register_in_tutoria(id_student, name_student, id_tutoria)  
            if exito:
                flash("Te has registrado exitosamente.", "success")
            else:
                flash("No fue posible registrarte.", "danger")
    else:
        flash("La tutoría no fue encontrada.", "danger")

    return redirect(url_for('tutorial.getListTutorials'))


@tutorial.route('/tutorial/tutor_tutorials')
@login_or_role_required('Tutor')
def listTutorTutorials():
    tutor_id = session.get('user_id')

    if not tutor_id:
        flash("No se pudo obtener el ID del tutor.", "danger")
        return redirect(url_for('tutorial.getListTutorials'))

    search = request.args.get('search', '').lower()
    sort = request.args.get('sort')

    tutorias = firebase_repo.get_tutorials_by_tutor(tutor_id)

    if search:
        tutorias = [
            t for t in tutorias
            if search in t.title.lower()
            or search in t.subject.lower()
            or search in t.description.lower()
        ]
    
    if sort == "asc":
        tutorias.sort(key=lambda t:  t.date)
    elif sort == "desc":
        tutorias.sort(key=lambda t:  t.date, reverse=True)

    return render_template('tutor_tutorials.html', tutorias=tutorias)

@tutorial.route('/tutorial/<id>/cancel', methods=['POST'])
@login_or_role_required('Tutor')
def cancel_tutorial(id):
    tutorial = firebase_repo.get_tutorial_by_id(id)  # Get tutorial from Firebase
    if not tutorial:
        flash("Tutoría no encontrada.", "danger")
        return redirect(url_for('tutorial.listTutorTutorials'))
    
    # Get confirmation from the request
    if request.form.get('confirm') != 'true':
        flash("Por favor confirme la cancelación de la tutoría.", "warning")
        return redirect(url_for('tutorial.getTutoriaById', id=id, user_role='tutor'))
    
    # Cancel the tutorial in Firebase
    if firebase_repo.cancel_tutorial(id):
        # Notify all enrolled students
        for student in tutorial.student_list:
            email_data = {
                "username": student["name"],
                "emailTo": "sebasbose@gmail.com",  # TODO: Replace with actual student email
                "tutorial": tutorial.title,
            }
            if not send_email_notification("tutorialCancelled", email_data):
                log_audit(
                    user=student["name"],
                    action_type=AuditActionType.CONTENT_UPDATE,
                    details=f"Failed to send cancellation notification for tutorial: {tutorial.title}",
                )
        
        flash("Tutoría cancelada exitosamente.", "success")
    else:
        flash("Error al cancelar la tutoría.", "danger")
    
    return redirect(url_for('tutorial.listTutorTutorials'))

def measure_time_to_tutorial(id):
    tutorial = firebase_repo.get_tutorial_by_id(id)
    present = get_current_datetime()

    date_str = tutorial.date.strip()
    time_str = tutorial.start_time.strip()[:5] 
    
    future = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
    time_difference = future - present
    return time_difference.total_seconds()/60  # minutes

