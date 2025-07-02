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
@patch('app.controllers.review_controller.delete_review')
def test_delete_review_existing(mock_delete_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock successful deletion
    mock_delete_review.return_value = "Review deleted successfully"
    
    response = client.post('/delete-review/test_tutoria/1', follow_redirects=True)
    assert response.status_code == 200

@patch('app.routes.review_routes.FirebaseTutoringRepository')
@patch('app.controllers.review_controller.delete_review')
def test_delete_review_non_existent(mock_delete_review, mock_firebase_repo, client):
    # Mock repository instance and its method
    mock_repo_instance = MagicMock()
    mock_repo_instance.get_tutoria_by_id.return_value = get_mock_tutorial()
    mock_firebase_repo.return_value = mock_repo_instance
    
    # Mock error when review doesn't exist
    mock_delete_review.return_value = "Review not found"

    response = client.post('/delete-review/test_tutoria/999', follow_redirects=True)
    assert response.status_code == 200

@patch('app.models.review_model.get_all_reviews')
@patch('app.models.repositories.users.firebase_user_repository.FirebaseUserRepository')
def test_comment_not_appearing_after_deletion(mock_user_repo, mock_get_all_reviews, client):
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {'profile_picture_url': ''}
    mock_user_repo.return_value = mock_user_instance
    
    # After deletion - only one review should remain
    mock_get_all_reviews.return_value = [
        {"review_id": 2, "student_id": "2", "tutor_id": "2", "comment": "Bien.", "rating": 4, "date": "2025-01-01", "replies": []},
    ]

    response = client.get('/comments/')
    assert response.status_code == 200
    data = response.get_data(as_text=True)
    assert "Buen tutor!" not in data
