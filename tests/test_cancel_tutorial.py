import pytest
from flask import session
from app import app as flask_app
from unittest.mock import patch, MagicMock

@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        with flask_app.app_context():
            yield client

@patch("app.controllers.tutorial_controller.firebase_repo")
@patch("app.controllers.tutorial_controller.send_email_notification")
def test_cancel_tutorial_success(mock_send_email, mock_repo, client):
    # Simular una tutoría existente con estudiantes
    tutorial = MagicMock()
    tutorial.student_list = [{"name": "Student 1"}, {"name": "Student 2"}]
    tutorial.title = "Tutoría de prueba"
    mock_repo.get_tutoria_by_id.return_value = tutorial
    mock_repo.cancel_tutorial.return_value = True
    mock_send_email.return_value = True

    with client.session_transaction() as sess:
        sess["role"] = "Tutor"
        sess["user_id"] = "tutor123"

    response = client.post("/tutorial/123/cancel", data={"confirm": "true"}, follow_redirects=True)

    assert b"Tutor\xc3\xada cancelada exitosamente." in response.data
    assert mock_repo.cancel_tutorial.called
    assert mock_send_email.call_count == 2

@patch("app.controllers.tutorial_controller.firebase_repo")
def test_cancel_tutorial_not_found(mock_repo, client):
    mock_repo.get_tutoria_by_id.return_value = None

    with client.session_transaction() as sess:
        sess["role"] = "Tutor"
        sess["user_id"] = "tutor123"

    response = client.post("/tutorial/999/cancel", data={"confirm": "true"}, follow_redirects=True)

    assert b"Tutor\xc3\xada no encontrada." in response.data

@patch("app.controllers.tutorial_controller.firebase_repo")
@patch("app.controllers.tutorial_controller.send_email_notification")
def test_cancel_tutorial_email_fail(mock_send_email, mock_repo, client):
    tutorial = MagicMock()
    tutorial.student_list = [{"name": "Student"}]
    tutorial.title = "Tutoría de prueba"
    mock_repo.get_tutoria_by_id.return_value = tutorial
    mock_repo.cancel_tutorial.return_value = True
    mock_send_email.return_value = False  # Simula falla en el correo

    with client.session_transaction() as sess:
        sess["role"] = "Tutor"
        sess["user_id"] = "tutor123"

    response = client.post("/tutorial/123/cancel", data={"confirm": "true"}, follow_redirects=True)

    assert b"Tutor\xc3\xada cancelada exitosamente." in response.data
    assert mock_send_email.call_count == 1
