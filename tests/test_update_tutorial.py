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

# -----------------------------
# UNIT TESTS AL REPO
# -----------------------------

def test_update_existing_tutorial(repo):
    tutorial_id = 1
    updated_data = {
        'title_tutoring': 'Tutoria de C++ Avanzado',
        'subject': 'Programación III',
        'date': '2025-10-10',
        'start_time': '11:00',
        'description': 'Temas avanzados de C++',
        'method': 'Presencial',
        'capacity': 5
    }

    result = repo.update_tutorial(tutorial_id, updated_data)
    updated = repo.get_tutorial_by_id(tutorial_id)

    assert result is True
    assert updated.title == 'Tutoria de C++ Avanzado'
    assert updated.subject == 'Programación III'
    assert updated.date == '2025-10-10'
    assert updated.start_time == '11:00'
    assert updated.description == 'Temas avanzados de C++'
    assert updated.method == 'Presencial'
    assert updated.capacity == 5


def test_update_nonexistent_tutorial(repo):
    updated_data = {
        'title_tutoring': 'Inexistente',
        'subject': 'Fantasía'
    }
    result = repo.update_tutorial(999, updated_data)
    assert result is False

def test_partial_update_tutorial(repo):
    tutorial_id = 2
    original = repo.get_tutorial_by_id(tutorial_id)
    updated_data = {
        'description': 'Descripción actualizada solamente'
    }

    repo.update_tutorial(tutorial_id, updated_data)
    updated = repo.get_tutorial_by_id(tutorial_id)

    assert updated.description == 'Descripción actualizada solamente'
    assert updated.title == original.title
    assert updated.subject == original.subject

# -----------------------------
# TEST FUNCIONAL DE RUTA /tutorial/<id>/edit
# -----------------------------

# NOTA:
# Este test funcional está comentado porque actualmente usamos un repositorio mock
# sin persistencia compartida entre instancias. El POST modifica una instancia
# que no es la misma que usamos luego para verificar.
# Cuando conectemos el backend real (DB o repo compartido), este test será válido.
# Por ahora, los tests unitarios sobre el repo sí validan el comportamiento correctamente.

# def test_update_tutorial_route(client):
#     response = client.post('/tutorial/1/edit', data={
#         'title_tutoring': 'Nueva Tutoria Editada',
#         'subject': 'Álgebra Lineal',
#         'date': '2025-12-01',
#         'start_time': '15:30',
#         'description': 'Editamos esta tutoría desde test.',
#         'method': 'Virtual',
#         'capacity': 10
#     }, follow_redirects=True)

#     assert response.status_code == 200
#     assert b'Tutoria' in response.data or b'tutorias' in response.data

#     repo = Tutorial_mock_repo()
#     tutoria = repo.get_tutorial_by_id(1)
#     assert tutoria.title != 'Tutoria de C++'
#     assert tutoria.title == 'Nueva Tutoria Editada'
