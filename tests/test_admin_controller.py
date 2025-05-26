import pytest
from flask import url_for, template_rendered
from unittest.mock import patch, MagicMock
from app.controllers.admin_controller import admin_bp, admin_required
from app.models.repositories.users.firebase_user_repository import FirebaseUserRepository
from app.models.services.email_service import SMTPEmailService
from contextlib import contextmanager

# Mock the FirebaseUserRepository
@pytest.fixture
def mock_user_repo():
    with patch('app.controllers.admin_controller.user_repo') as mock:
        yield mock

# Mock the SMTPEmailService
@pytest.fixture
def mock_email_service():
    with patch('app.controllers.admin_controller.SMTPEmailService') as mock:
        mock_instance = MagicMock()
        mock.return_value = mock_instance
        yield mock_instance

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

# Test admin_required decorator
def test_admin_required_decorator():
    @admin_required
    def test_function():
        return "success"
    
    # Since the decorator is currently a TODO, it should just pass through
    assert test_function() == "success"

# Test dashboard route
def test_dashboard_route(client, app):
    with captured_templates(app) as templates:
        response = client.get('/admin/')
        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == 'admin/dashboard.html'

# Test users GET route
def test_users_get_route(client, app, mock_user_repo):
    # Mock the get_all_users method
    mock_users = [
        {'email': 'test1@example.com', 'status': True},
        {'email': 'test2@example.com', 'status': False}
    ]
    mock_user_repo.get_all_users.return_value = mock_users

    with captured_templates(app) as templates:
        response = client.get('/admin/users')
        assert response.status_code == 200
        template, context = templates[0]
        assert template.name == 'admin/users.html'
        assert 'users' in context
        assert context['users'] == mock_users
        mock_user_repo.get_all_users.assert_called_once()

# Test users POST route - successful update
def test_users_post_route_success(client, mock_user_repo):
    mock_user_repo.update_user_status.return_value = True
    
    response = client.post('/admin/users', 
                          json={'email': 'test@example.com', 'status': True})
    
    assert response.status_code == 200
    assert response.json['success'] is True
    mock_user_repo.update_user_status.assert_called_once_with('test@example.com', True)

# Test users POST route - missing parameters
def test_users_post_route_missing_params(client):
    response = client.post('/admin/users', json={})
    assert response.status_code == 400
    assert response.json['success'] is False
    assert 'Missing parameters' in response.json['error']

# Test users POST route - update failure
def test_users_post_route_failure(client, mock_user_repo):
    mock_user_repo.update_user_status.return_value = False
    
    response = client.post('/admin/users', 
                          json={'email': 'test@example.com', 'status': True})
    
    assert response.status_code == 500
    assert response.json['success'] is False
    assert 'Failed to update status' in response.json['error']

# Test ban notification email - success
def test_ban_notification_email_success(client, mock_email_service):
    mock_email_service.send_email.return_value = True
    
    response = client.post('/admin/send-ban-email', 
                          json={'email': 'test@example.com'})
    
    assert response.status_code == 200
    assert response.json['success'] is True
    assert 'Usuario notificado con éxito' in response.json['message']
    mock_email_service.send_email.assert_called_once()

# Test ban notification email - missing email
def test_ban_notification_email_missing_email(client):
    response = client.post('/admin/send-ban-email', json={})
    assert response.status_code == 200
    assert response.json['success'] is False
    assert 'Email no proporcionado' in response.json['error']

# Test other basic routes
def test_tutorials_route(client, app):
    with captured_templates(app) as templates:
        response = client.get('/admin/tutorials')
        assert response.status_code == 200
        assert b'Tutorials' in response.data

def test_reviews_route(client, app):
    with captured_templates(app) as templates:
        response = client.get('/admin/reviews')
        assert response.status_code == 200
        assert b'Reviews' in response.data

def test_logs_route(client, app):
    with captured_templates(app) as templates:
        response = client.get('/admin/logs')
        assert response.status_code == 200
        assert b'Logs' in response.data

def test_settings_route(client, app):
    with captured_templates(app) as templates:
        response = client.get('/admin/settings')
        assert response.status_code == 200
        assert b'Settings' in response.data 