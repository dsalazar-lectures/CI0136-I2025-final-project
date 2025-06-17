import pytest
from unittest.mock import MagicMock, patch
from app.services.ban_notification_service.ban_notification_types import BehavioralViolation

@pytest.fixture
def mock_email_service():
    return MagicMock()

@pytest.fixture
def behavior_notification(mock_email_service):
    notification = BehavioralViolation()
    notification.email_service = mock_email_service
    return notification

def test_behavior_notification_sends_email(behavior_notification):
    test_email = "test@example.com"
    behavior_notification.notify(test_email)
    
    behavior_notification.email_service.send_email.assert_called_once_with(
        to=test_email,
        subject="Account Ban Notification",
        template="ban_notification_email.html",
        template_data={"reason": "behavior"}
    )

def test_behavior_notification_invalid_email(behavior_notification):
    with pytest.raises(ValueError):
        behavior_notification.notify("")

    with pytest.raises(ValueError):
        behavior_notification.notify(None)

@patch('app.services.ban_notification_service.ban_notification_types.EmailService')
def test_behavior_notification_email_service_exception(mock_email_service):
    mock_email_service.send_email.side_effect = Exception("Email service error")
    notification = BehaviorBanNotification()
    notification.email_service = mock_email_service
    
    with pytest.raises(Exception) as exc_info:
        notification.notify("test@example.com")
    assert str(exc_info.value) == "Email service error"
