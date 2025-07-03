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
def test_user_can_select_rating_from_1_to_5(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock successful review submission
    mock_send_review.return_value = "Review sent successfully"
    
    for rating in range(1, 6):
        response = client.post('/send-review/test_tutoria', data={
            'student_id': 'EstudianteTest',
            'tutor_id': 'TutorTest',
            'session_id': 'SesionTest',
            'review_id': str(10000 + rating),
            'rating': str(rating),
            'comment': f'Calificación de {rating} estrellas.'
        }, follow_redirects=True)

        assert response.status_code == 200

@patch('app.models.review_model.get_all_reviews')
@patch('app.models.repositories.users.firebase_user_repository.FirebaseUserRepository')
def test_rating_appears_with_comment(mock_user_repo, mock_get_reviews, client):
    # Mock review with rating
    mock_get_reviews.return_value = [{
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'SesionTest',
        'review_id': 55557,
        'rating': 4,
        'comment': 'Comentario con calificación.',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {'profile_picture_url': ''}
    mock_user_repo.return_value = mock_user_instance

    response = client.get('/comments/')
    data = response.get_data(as_text=True)
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.send_review')
def test_comment_without_rating_is_rejected(mock_send_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock validation error for missing rating
    mock_send_review.return_value = "Rating is required"
    
    response = client.post('/send-review/test_tutoria', data={
        'student_id': 'EstudianteTest',
        'tutor_id': 'TutorTest',
        'session_id': 'SesionTest',
        'review_id': '55558',
        'rating': '',  # sin calificación
        'comment': 'Comentario sin calificación.'
    }, follow_redirects=True)

    assert response.status_code == 200
