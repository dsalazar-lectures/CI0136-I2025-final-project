import pytest
from app import app
from app.models.repositories.tutorial.repoTutorials import Tutorial_mock_repo

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture
def repo():
    return Tutorial_mock_repo()

def test_create_tutorial_count(repo):
    # Se asegura de que la cantidad de tutorías aumente al crear una nueva
    initial_count = len(repo.tutorias)
    # Se crea una nueva tutoría
    new = repo.create_tutorial(
        "Python Básico", 3, "Pedro Ramírez", "Programación I", "2025-11-01",
        "09:00", "Introducción a Python", "Virtual", 20
    )
    assert len(repo.tutorias) == initial_count + 1

def test_create_tutorial_values_confirmation(repo):
    # Se crea una nueva tutoría
    new = repo.create_tutorial(
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

def test_create_and_get_tutorial_by_id(repo):
    # Se crea una nueva tutoría
    new = repo.create_tutorial(
        "Python Básico", 3, "Pedro Ramírez", "Programación I", "2025-11-01",
        "09:00", "Introducción a Python", "Virtual", 20
    )
    # Recuperar la tutoría por su ID
    found = repo.get_tutorial_by_id(new.id)
    assert found is not None
    assert found.title == "Python Básico"
    assert found.tutor == "Pedro Ramírez"
    assert found.subject == "Programación I"
    assert found.date == "2025-11-01"
    assert found.start_time == "09:00"
    assert found.description == "Introducción a Python"
    assert found.method == "Virtual"
    assert found.capacity == 20

def test_create_tutorial_request(client):
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
    assert '/tutorial/' in response.headers['Location']