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

def get_mock_tutorial():
    """Helper function to create a mock tutorial"""
    return Tutorial(
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

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.send_review')
def test_valid_review_submission(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock successful review submission
    mock_send_review.return_value = "Review sent successfully"
    
    response = client.post('/send-review/test_tutoria', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55555',
        'rating': '4',
        'comment': 'Buen tutor.'
    }, follow_redirects=True)
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.send_review') 
def test_rating_above_maximum(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock validation error for rating above maximum
    mock_send_review.return_value = "Rating must be between 1 and 5"
    
    response = client.post('/send-review/test_tutoria', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55556',
        'rating': '6',
        'comment': 'Muy bueno'
    }, follow_redirects=True)
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.send_review')
def test_rating_not_a_number(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock validation error for non-numeric rating
    mock_send_review.return_value = "Rating must be a valid number"
    
    response = client.post('/send-review/test_tutoria', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55557',
        'rating': 'abc',
        'comment': 'No es número'
    }, follow_redirects=True)
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.send_review')
def test_empty_rating(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock validation error for empty rating
    mock_send_review.return_value = "Rating cannot be empty"
    
    response = client.post('/send-review/test_tutoria', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55558',
        'comment': 'Falta rating'
    }, follow_redirects=True)
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.send_review')
def test_empty_comment(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock validation error for empty comment
    mock_send_review.return_value = "Comment cannot be empty"
    
    response = client.post('/send-review/test_tutoria', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'Sesion de Java',
        'review_id': '55559',
        'rating': '4',
        'comment': '   '
    }, follow_redirects=True)
    assert response.status_code == 200
