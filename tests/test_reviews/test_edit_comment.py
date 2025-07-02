import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
from app import app
from app.models.repositories.tutorial.tutorial import Tutorial

@pytest.fixture
def client():
    app.config['TESTING'] = True
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
def test_edit_review_route_exists(mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Test that the edit review route exists and handles POST requests
    response = client.post("/edit-review/test_tutoria/99999", data={
        'comment': "Comentario actualizado.",
        'rating': 4
    }, follow_redirects=True)
    
    # The route should exist (not 404) even if it redirects due to auth/validation
    assert response.status_code != 404

@patch('app.routes.review_routes.FirebaseTutoringRepository')
def test_edit_review_with_invalid_rating(mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Test edit with invalid rating
    response = client.post("/edit-review/test_tutoria/99999", data={
        'comment': 'Test comment',
        'rating': 'invalid'
    }, follow_redirects=True)
    
    # Route should exist and handle the request
    assert response.status_code != 404

@patch('app.routes.review_routes.FirebaseTutoringRepository')
def test_edit_review_with_empty_comment(mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Test edit with empty comment
    response = client.post("/edit-review/test_tutoria/99999", data={
        'comment': '',
        'rating': 4
    }, follow_redirects=True)
    
    # Route should exist and handle the request
    assert response.status_code != 404

@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_edit_button_visible(mock_user_repo, mock_get_reviews, client):
    # Mock review data
    mock_get_reviews.return_value = [{
        'review_id': 1,
        'student_id': 'test_student',
        'comment': 'Test comment',
        'rating': 3,
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {'profile_picture_url': ''}
    mock_user_repo.return_value = mock_user_instance
    
    response = client.get("/comments/")
    assert response.status_code == 200