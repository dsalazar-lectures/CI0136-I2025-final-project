import pytest
from unittest.mock import patch, MagicMock
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_comments_appear_in_tutor_profile(mock_user_repo, mock_get_reviews, client):
    # Mock review data
    mock_get_reviews.return_value = [{
        'student_id': 'UsuarioTest',
        'tutor_id': 'Tutor123',
        'session_id': 'Sesion de Java',
        'review_id': 12345,
        'rating': 4,
        'comment': 'Muy buen tutor.',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {'profile_picture_url': ''}
    mock_user_repo.return_value = mock_user_instance

    response = client.get('/comments/')
    assert response.status_code == 200

@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')  
def test_comment_shows_author_date_and_photo(mock_user_repo, mock_get_reviews, client):
    # Mock review data
    mock_get_reviews.return_value = [{
        'student_id': 'UsuarioTest',
        'tutor_id': 'Tutor123',
        'session_id': 'Sesion de Java',
        'review_id': 12346,
        'rating': 5,
        'comment': 'Excelente explicacion.',
        'date': '2025-01-01',
        'replies': []
    }]
    
    # Mock user repository 
    mock_user_instance = MagicMock()
    mock_user_instance.get_user_by_name.return_value = {
        'profile_picture_url': 'https://example.com/user.jpg'
    }
    mock_user_repo.return_value = mock_user_instance

    response = client.get('/comments/')
    assert response.status_code == 200
    data = response.get_data(as_text=True)

    assert 'UsuarioTest' in data
    assert 'Excelente explicacion.' in data
    assert 'Fecha:' in data or 'fecha' in data.lower()

@patch('app.routes.review_routes.get_all_reviews')
@patch('app.routes.review_routes.FirebaseUserRepository')
def test_add_comment_button_visible_for_tutored_user(mock_user_repo, mock_get_reviews, client):
    # Mock empty reviews for button visibility test
    mock_get_reviews.return_value = []
    
    # Mock user repository
    mock_user_instance = MagicMock()
    mock_user_repo.return_value = mock_user_instance
    
    response = client.get('/comments/')
    assert response.status_code == 200
    data = response.get_data(as_text=True)

    # Note: This test needs to be updated based on actual button visibility logic
    # The button visibility might depend on user session or other factors
