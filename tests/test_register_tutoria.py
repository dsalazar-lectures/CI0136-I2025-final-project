import pytest   
from app.models.repositories.tutorial.tutorial import Tutorial  
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository

def test_register_tutoria_success(client, mocker):
    # Mock the method get_tutoria_by_id to simulate a valid response.
    mocker.patch.object(FirebaseTutoringRepository, 'get_tutoria_by_id', return_value=Tutorial(
        id_tutoring="2",
        title_tutoring="Tutoria de C++",
        tutor_id="t1",
        tutor="Juan Pérez",
        subject="Programación II",
        date="2025-10-01",
        start_time="10:00",
        description="Reforzar lo aprendido sobre C++",
        method="Virtual",
        capacity=10,
        student_list=[]
    ))

    # Mock the method register_in_tutoria to simulate a successful registration.
    mocker.patch.object(FirebaseTutoringRepository, 'register_in_tutoria', return_value=True)

    
    with client.session_transaction() as session:
        session['user_id'] = '12345'
        session['name'] = 'Test Student'
        session['role'] = 'Student'

    # Simulate an authenticated user.
    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': '2'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b"Te has registrado exitosamente." in response.data

def test_tutoria_no_slots_display(client, mocker):
    
    mocker.patch.object(FirebaseTutoringRepository, 'get_list_tutorials', return_value=[{
        "id_tutoring": "1",
        "title_tutoring": "Tutoria de C++",
        "tutor_id": "t1",
        "tutor": "Juan Pérez",
        "subject": "Programación II",
        "date": "2025-05-25",
        "start_time": "10:00",
        "description": "Reforzar conceptos básicos de programación.",
        "method": "Virtual",
        "capacity": 3,
        "student_list": [
            {"id": "otro_estudiante", "name": "A"},
            {"id": "estudiante_123", "name": "Luis Fernández"},
            {"id": "estudiante_456", "name": "María López"}
        ]
    }])

    response = client.get('/tutorial/list')
    html = response.get_data(as_text=True)

    assert "Tutoría sin cupo" in html
    assert "Inscribirme" not in html

def test_register_tutoria_already_registered(client, mocker):
    
    mocker.patch.object(FirebaseTutoringRepository, 'register_in_tutoria', return_value=False)

    mocker.patch.object(FirebaseTutoringRepository, 'get_tutoria_by_id', return_value=Tutorial(
        id_tutoring="3",
        title_tutoring="Tutoria de Java",
        tutor_id="t2",
        tutor="Carlos Matamoros",
        subject="Programación Avanzada",
        date="2025-10-01",
        start_time="10:00",
        description="Reforzar lo aprendido sobre Java",
        method="Virtual",
        capacity=10,
        student_list=[{"id": "1", "name": "Carlos Matamoros"}]
    ))

    with client.session_transaction() as session:
        session['user_id'] = '1'
        session['name'] = 'Carlos Matamoros'
        session['role'] = 'Student'

    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': '3'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert "Ya estás registrado en esta tutoría.".encode("utf-8") in response.data

def test_view_tutorial_slots(client, mocker):
   
    with client.session_transaction() as session:
        session['user_id'] = '123'
        session['name'] = 'Estudiante de Prueba'
        session['role'] = 'Student'

    tutoria_mock = Tutorial(
        id_tutoring="1",
        title_tutoring="Tutoria de Python",
        tutor_id="t1",
        tutor="Ana Pérez",
        subject="Programación Avanzada",
        date="2025-05-30",
        start_time="15:00",
        description="Aprender conceptos avanzados de Python.",
        method="Virtual",
        capacity=5,
        student_list=[{"id": "estudiante_123", "name": "Luis Fernández"},
                      {"id": "estudiante_456", "name": "María López"}]
    )

    mocker.patch.object(FirebaseTutoringRepository, 'get_tutoria_by_id', return_value=tutoria_mock)

    response = client.get('/tutorial/1')
    html = response.get_data(as_text=True)

    assert "<strong>Cupos disponibles:</strong> 3" in html

