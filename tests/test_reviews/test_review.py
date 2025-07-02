import pytest
from unittest.mock import patch, MagicMock
from app import app
from app.models.review_model import ReviewManager
from app.models.repositories.tutorial.tutorial import Tutorial

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client

@pytest.fixture
def mock_review_manager():
    with patch('app.models.review_model.ReviewManager') as mock:
        yield mock

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.models.review_model.get_all_reviews')
@patch('app.controllers.review_controller.send_review')
def test_send_review(mock_send_review, mock_get_reviews, mock_firebase_repo, client):
    # Mock tutorial data
    mock_tutorial = Tutorial(
        id_tutoring="test_tutoria",
        title_tutoring="Test Tutorial",
        tutor_id="TutorTest",
        tutor="Tutor Name",
        subject="Test Subject",
        date="2025-01-01",
        start_time="10:00",
        description="Test Description",
        method="Virtual",
        capacity=10
    )
    
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = mock_tutorial
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock the send_review function to return a successful response
    mock_send_review.return_value = "Review sent successfully"
    
    # Mock the get_all_reviews to return a review after sending
    mock_get_reviews.return_value = [{
        "student_id": "EstudianteTest",
        "tutor_id": "TutorTest", 
        "session_id": "Sesion de Prueba",
        "review_id": 11111,
        "rating": 4,
        "comment": "Muy buena tutoría",
        "date": "01/01/2025"
    }]

    review_data = {
        "student_id": "EstudianteTest",
        "tutor_id": "TutorTest",
        "session_id": "Sesion de Prueba",
        "review_id": 11111,
        "rating": "4",
        "comment": "Muy buena tutoría"
    }

    res = client.post("/send-review/test_tutoria", data=review_data, follow_redirects=True)
    assert res.status_code == 200

@patch('app.models.review_model.get_all_reviews')
def test_filter_reviews_by_session(mock_get_reviews, client):
    mock_get_reviews.return_value = [
        {
            "student_id": "A",
            "tutor_id": "T1",
            "session_id": "Sesion A",
            "review_id": 1,
            "rating": 5,
            "comment": "Buenísimo",
            "date": "01/01/2025"
        },
        {
            "student_id": "B",
            "tutor_id": "T2",
            "session_id": "Sesion B",
            "review_id": 2,
            "rating": 4,
            "comment": "Regular",
            "date": "01/01/2025"
        }
    ]

    res = client.get("/comments/")
    html = res.get_data(as_text=True)
    assert res.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.delete_review')
def test_delete_review(mock_delete_review, mock_firebase_repo, client):
    # Mock tutorial data
    mock_tutorial = Tutorial(
        id_tutoring="test_tutoria",
        title_tutoring="Test Tutorial",
        tutor_id="TutorTest",
        tutor="Tutor Name",
        subject="Test Subject",
        date="2025-01-01",
        start_time="10:00",
        description="Test Description",
        method="Virtual",
        capacity=10
    )
    
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = mock_tutorial
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock successful deletion
    mock_delete_review.return_value = "Review deleted successfully"
    
    res = client.post("/delete-review/test_tutoria/333", follow_redirects=True)
    assert res.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.add_reply')
@patch('app.models.review_model.get_review_by_id')
def test_add_reply(mock_get_review, mock_add_reply, mock_firebase_repo, client):
    # Mock tutorial data
    mock_tutorial = Tutorial(
        id_tutoring="test_tutoria",
        title_tutoring="Test Tutorial",
        tutor_id="T4",
        tutor="Tutor Name",
        subject="Test Subject",
        date="2025-01-01",
        start_time="10:00",
        description="Test Description",
        method="Virtual",
        capacity=10
    )
    
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = mock_tutorial
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock the review after adding reply
    mock_review_with_reply = {
        "student_id": "D",
        "tutor_id": "T4",
        "session_id": "Sesion Respuesta",
        "review_id": 444,
        "rating": 5,
        "comment": "Esperando respuesta",
        "date": "01/01/2025",
        "replies": [{
            "tutor_id": "T4",
            "comment": "Gracias por tu comentario",
            "date": "01/01/2025"
        }]
    }
    
    mock_get_review.return_value = mock_review_with_reply
    mock_add_reply.return_value = "Reply added successfully"

    reply_data = {
        "tutor_id": "T4",
        "comment": "Gracias por tu comentario"
    }

    res = client.post("/reply-review/test_tutoria/444", data=reply_data, follow_redirects=True)
    assert res.status_code == 200
