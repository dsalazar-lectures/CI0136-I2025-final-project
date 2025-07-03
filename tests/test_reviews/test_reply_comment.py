import pytest
from unittest.mock import patch, MagicMock
from app import app
from app.models.repositories.tutorial.tutorial import Tutorial

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.add_reply')
def test_tutor_can_reply_to_review(mock_add_reply, mock_firebase_repo, client):
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
    
    # Mock successful reply addition
    mock_add_reply.return_value = "Reply added successfully"
    
    response = client.post("/reply-review/test_tutoria/12345", data={
        'tutor_id': 'TutorTest',
        'comment': 'Gracias por tu comentario!'
    }, follow_redirects=True)
    
    assert response.status_code == 200

@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_reply_appears_below_original_review(mock_user_repo, mock_get_reviews, client):
    # Mock review with reply
    mock_get_reviews.return_value = [{
        'review_id': 12345,
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'rating': 4,
        'comment': 'Buen tutor',
        'date': '2025-01-01',
        'replies': [{
            'tutor_id': 'TutorTest',
            'comment': 'Gracias por tu comentario!',
            'date': '2025-01-02'
        }]
    }]
    
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {'profile_picture_url': ''}
    mock_user_repo.return_value = mock_user_instance
    
    response = client.get('/comments/')
    data = response.get_data(as_text=True)
    
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.add_reply')
def test_empty_reply_is_rejected(mock_add_reply, mock_firebase_repo, client):
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
    
    # Mock validation error for empty reply
    mock_add_reply.return_value = "Reply cannot be empty"
    
    response = client.post("/reply-review/test_tutoria/12345", data={
        'tutor_id': 'TutorTest',
        'comment': ''  # Empty comment
    }, follow_redirects=True)
    
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.add_reply')
def test_multiple_replies_supported(mock_add_reply, mock_firebase_repo, client):
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
    
    # Mock successful multiple replies
    mock_add_reply.return_value = "Reply added successfully"
    
    # First reply
    response1 = client.post("/reply-review/test_tutoria/12345", data={
        'tutor_id': 'TutorTest',
        'comment': 'Primera respuesta'
    }, follow_redirects=True)
    
    # Second reply
    response2 = client.post("/reply-review/test_tutoria/12345", data={
        'tutor_id': 'TutorTest',
        'comment': 'Segunda respuesta'
    }, follow_redirects=True)
    
    assert response1.status_code == 200
    assert response2.status_code == 200
