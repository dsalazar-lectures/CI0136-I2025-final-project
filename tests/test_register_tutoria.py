import pytest  # Importa pytest para manejar las pruebas
from app.models.repositories.tutorial.repoTutorials import Tutorial_mock_repo  # Importa el repositorio mock para pruebas
from app.models.repositories.tutorial.tutorial import Tutorial  # Importa la clase Tutorial

def test_register_tutoria_success(client):
    # Simula un usuario autenticado
    with client.session_transaction() as session:
        session['user_id'] = '12345'
        session['name'] = 'Test Student'
        session['role'] = 'Student'  # Agrega el rol necesario

    # Simula el registro en una tutoría
    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': '2'  # Cambia 'tutoria1' por un ID válido
    }, follow_redirects=True)  # Sigue la redirección

    assert response.status_code == 200  # Verifica que la solicitud sea exitosa
    assert b"Te has registrado exitosamente." in response.data  # Verifica el mensaje de éxito

def test_tutoria_sin_cupo_display(client, mocker):
    # Simular sesión del estudiante
    with client.session_transaction() as session:
        session['user_id'] = '123'
        session['name'] = 'Estudiante de Prueba'
        session['role'] = 'Student'

    # Simular una tutoría sin cupos
    tutoria_mock = Tutorial(
        id_tutoring="1",
        title_tutoring="Tutoria de C++",
        tutor_id="t1",
        tutor="Juan Pérez",
        subject="Programación II",
        date="2025-05-25",
        start_time="10:00",
        description="Reforzar conceptos básicos de programación.",
        method="Virtual",
        capacity=3,
        student_list=[{"id": "otro_estudiante", "name": "A"}, 
                      {"id": "estudiante_123", "name": "Luis Fernández"}, 
                      {"id": "estudiante_456", "name": "María López"}]
    )

    # Mock de list_tutorials para retornar la tutoría sin cupo
    mocker.patch("app.models.repositories.tutorial.repoTutorials.Tutorial_mock_repo.list_tutorials", return_value=[tutoria_mock])

    # Ir a la lista de tutorías
    response = client.get('/tutorial/list')
    html = response.get_data(as_text=True)

    # Verificar que se muestra el mensaje de "Tutoría sin cupo"
    assert "Tutoría sin cupo" in html

    # Verificar que el botón "Inscribirme" no aparece
    assert "Inscribirme" not in html

def test_register_tutoria_already_registered(client):
    # Simula un usuario autenticado
    with client.session_transaction() as session:
        session['user_id'] = '1'
        session['name'] = 'Carlos Matamoros'
        session['role'] = 'Student'

    # Simula el registro en una tutoría en la que ya está inscrito
    response = client.post('/tutorial/register_tutoria', data={
        'id_tutoria': '3'
    }, follow_redirects=True)  # Sigue la redirección

    # Depurar el contenido de la respuesta
    print(response.data.decode())

    assert response.status_code == 200  # Verifica que la solicitud sea exitosa
    assert "Ya estás registrado en esta tutoría." in response.data.decode()  # Verifica el mensaje de error

def test_view_tutorial_slots(client, mocker):
    # Simular sesión del estudiante
    with client.session_transaction() as session:
        session['user_id'] = '123'
        session['name'] = 'Estudiante de Prueba'
        session['role'] = 'Student'

    # Simular una tutoría con cupos disponibles
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

    # Mock de get_tutorial_by_id para retornar la tutoría
    mocker.patch("app.models.repositories.tutorial.repoTutorials.Tutorial_mock_repo.get_tutorial_by_id", return_value=tutoria_mock)

    # Ir a la página de detalles de la tutoría
    response = client.get('/tutorial/1')
    html = response.get_data(as_text=True)


    # Verificar que los cupos disponibles se muestran correctamente
    assert "<strong>Cupos disponibles:</strong> 3" in html

