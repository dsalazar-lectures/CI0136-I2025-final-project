import pytest
from unittest.mock import patch, MagicMock
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.secret_key = 'test_secret_key'
    with app.test_client() as client:
        yield client


@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_review_with_student_profile_picture(mock_user_repo, mock_get_reviews, client):
    """Test that student profile pictures are displayed in reviews"""
    
    # Mock review data
    mock_reviews = [{
        'review_id': 1,
        'student_id': 'test_student',
        'tutor_id': 'test_tutor', 
        'session_id': 'Test Session',
        'rating': 5,
        'comment': 'Great tutorial!',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {
        'profile_picture_url': 'https://example.com/student_pic.jpg'
    }
    mock_user_repo.return_value = mock_user_instance
    
    mock_get_reviews.return_value = mock_reviews
    
    response = client.get('/comments/')
    
    assert response.status_code == 200
    # Verify the user repository was called to get student profile picture
    mock_user_instance.get_user_by_name.assert_called_with('test_student')


@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_review_with_tutor_profile_picture_in_reply(mock_user_repo, mock_get_reviews, client):
    """Test that tutor profile pictures are displayed in review replies"""
    
    # Mock review data with replies
    mock_reviews = [{
        'review_id': 1,
        'student_id': 'test_student',
        'tutor_id': 'test_tutor',
        'session_id': 'Test Session',
        'rating': 5,
        'comment': 'Great tutorial!',
        'date': '2025-01-01',
        'replies': [{
            'reply_id': 1,
            'tutor_id': 'test_tutor',
            'reply_text': 'Thank you for the feedback!',
            'date': '2025-01-02'
        }]
    }]
    
    # Mock user repository to return different pics for student and tutor
    mock_user_instance = MagicMock()
    def mock_get_user(name):
        if name == 'test_student':
            return {'profile_picture_url': 'https://example.com/student_pic.jpg'}
        elif name == 'test_tutor':
            return {'profile_picture_url': 'https://example.com/tutor_pic.jpg'}
        return {}
    
    mock_user_instance.get_user_by_name.side_effect = mock_get_user
    mock_user_repo.return_value = mock_user_instance
    
    mock_get_reviews.return_value = mock_reviews
    
    response = client.get('/comments/')
    
    assert response.status_code == 200
    # Verify both student and tutor profile pictures were fetched
    mock_user_instance.get_user_by_name.assert_any_call('test_student')
    mock_user_instance.get_user_by_name.assert_any_call('test_tutor')


@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_review_with_missing_profile_picture(mock_user_repo, mock_get_reviews, client):
    """Test handling when user profile picture is not available"""
    
    # Mock review data
    mock_reviews = [{
        'review_id': 1,
        'student_id': 'test_student',
        'tutor_id': 'test_tutor',
        'session_id': 'Test Session', 
        'rating': 5,
        'comment': 'Great tutorial!',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository to return user without profile picture
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {}  # No profile_picture_url field
    mock_user_repo.return_value = mock_user_instance
    
    mock_get_reviews.return_value = mock_reviews
    
    response = client.get('/comments/')
    
    assert response.status_code == 200
    # Should handle missing profile picture gracefully


@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_review_with_user_not_found(mock_user_repo, mock_get_reviews, client):
    """Test handling when user is not found in repository"""
    
    # Mock review data
    mock_reviews = [{
        'review_id': 1,
        'student_id': 'nonexistent_student',
        'tutor_id': 'test_tutor',
        'session_id': 'Test Session',
        'rating': 5,
        'comment': 'Great tutorial!',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository to return None for nonexistent user
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = None
    mock_user_repo.return_value = mock_user_instance
    
    mock_get_reviews.return_value = mock_reviews
    
    response = client.get('/comments/')
    
    assert response.status_code == 200
    # Should handle nonexistent user gracefully


@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_review_with_repository_exception(mock_user_repo, mock_get_reviews, client):
    """Test handling repository exceptions when fetching profile pictures"""
    
    # Mock review data
    mock_reviews = [{
        'review_id': 1,
        'student_id': 'test_student',
        'tutor_id': 'test_tutor',
        'session_id': 'Test Session',
        'rating': 5,
        'comment': 'Great tutorial!',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository to raise exception
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.side_effect = Exception("Database connection error")
    mock_user_repo.return_value = mock_user_instance
    
    mock_get_reviews.return_value = mock_reviews
    
    response = client.get('/comments/')
    
    assert response.status_code == 200
    # Should handle repository exceptions gracefully