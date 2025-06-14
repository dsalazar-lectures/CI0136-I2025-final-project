import pytest
import time
from app import app
from app.models.repositories.tutorial.repoTutorials import Tutorial_mock_repo
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def repoMock():
    return Tutorial_mock_repo()

@pytest.fixture
def repoFirebase():
    return FirebaseTutoringRepository()

def test_create_tutorial_count(repoMock):
    # Se asegura de que la cantidad de tutorías aumente al crear una nueva
    initial_count = len(repoMock.tutorias)
    # Se crea una nueva tutoría
    new = repoMock.create_tutorial(
        "Python Básico", 3, "Pedro Ramírez", "Programación I", "2025-11-01",
        "09:00", "Introducción a Python", "Virtual", 20
    )
    assert len(repoMock.tutorias) == initial_count + 1

def test_create_tutorial_values_confirmation(repoMock):
    # Se crea una nueva tutoría
    new = repoMock.create_tutorial(
        "Python Básico", 3, "Pedro Ramírez", "Programación I", "2025-11-01",
        "09:00", "Introducción a Python", "Virtual", 20
    )
    # Verifica que la nueva tutoría tenga los valores correctos
    assert new.title == "Python Básico"
    assert new.tutor == "Pedro Ramírez"
    assert new.subject == "Programación I"
    assert new.date == "2025-11-01"
    assert new.start_time == "09:00"
    assert new.description == "Introducción a Python"
    assert new.method == "Virtual"
    assert new.capacity == 20

def test_create_tutorial_values_confirmation_firebase(repoFirebase):
    # Se crea una nueva tutoría
    new = repoFirebase.create_tutorial(
        "Python Básico", 3, "Pedro Ramírez", "Programación I", "2025-11-01",
        "09:00", "Introducción a Python", "Virtual", 20
    )
    # Verifica que la nueva tutoría tenga los valores correctos
    assert new["title"] == "Python Básico"
    assert new["tutor"] == "Pedro Ramírez"
    assert new["subject"] == "Programación I"
    assert new["date"] == "2025-11-01"
    assert new["start_time"] == "09:00"
    assert new["description"] == "Introducción a Python"
    assert new["method"] == "Virtual"
    assert new["capacity"] == 20

def test_create_tutorial_request(client):
    # Simula un usuario loggeado con rol Tutor
    with client.session_transaction() as sess:
        sess['user_id'] = 99
        sess['name'] = 'Test Tutor'
        sess['role'] = 'Tutor'
        sess['email'] = 'test@tutor.com'

    # Simula una solicitud para crear una nueva tutoría
    response = client.post('/tutorial/create', data={
        'title_tutoring': 'Test Tutoring',
        'subject': 'Test Subject',
        'date': '2025-10-10',
        'start_time': '10:00',
        'description': 'Test Description',
        'method': 'Virtual',
        'capacity': 5
    })

    # Verifica que la respuesta sea una redirección
    assert response.status_code == 302
    # Verifica que la redirección sea a la página del tutorial creado
    assert '/tutorial' in response.headers['Location']