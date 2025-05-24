import pytest  # Importa pytest para manejar las pruebas
from app.models.repositories.tutorial.repoTutorials import Tutorial_mock_repo  # Importa el repositorio mock para pruebas

def test_register_tutoria_success(client):
    # Simula un usuario autenticado
    with client.session_transaction() as session:
        session['user_id'] = '12345'
        session['name'] = 'Test Student'
        session['role'] = 'Student'  # Agrega el rol necesario

    # Simula el registro en una tutoría
    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': '1'  # Cambia 'tutoria1' por un ID válido
    }, follow_redirects=True)  # Sigue la redirección

    assert response.status_code == 200  # Verifica que la solicitud sea exitosa
    assert b"Te has registrado exitosamente." in response.data  # Verifica el mensaje de éxito

def test_register_tutoria_no_slots(client):
    # Simula un usuario autenticado
    with client.session_transaction() as session:
        session['user_id'] = '12345'
        session['name'] = 'Test Student'

    # Simula el registro en una tutoría sin cupos
    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': 'tutoria_sin_cupos'
    })

    assert response.status_code == 200  # No redirige
    assert "No hay cupos disponibles para esta tutoría.".encode() in response.data  # Verifica el mensaje de error

def test_register_tutoria_already_registered(client):
    # Simula un usuario autenticado
    with client.session_transaction() as session:
        session['user_id'] = '12345'
        session['name'] = 'Test Student'

    # Simula el registro en una tutoría en la que ya está inscrito
    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': 'tutoria1'
    })

    assert response.status_code == 200  # No redirige
    assert "Ya estás registrado en esta tutoría.".encode() in response.data  # Verifica el mensaje de error