# -*- coding: utf-8 -*-
import pytest
from unittest.mock import MagicMock, patch
from app.services.ban_notification_service.ban_notification_types import BehavioralViolation

@pytest.fixture
def behavior_notification():
    with patch('app.services.ban_notification_service.ban_notification_types.BehavioralViolation.send_email') as mock_send:
        notification = BehavioralViolation()
        notification.send_email = mock_send
        yield notification

def test_behavior_notification_sends_email(behavior_notification):
    test_email = "test@example.com"
    behavior_notification.notify(test_email)
    
    behavior_notification.send_email.assert_called_once_with(
        test_email,
        behavior_notification.subject,
        behavior_notification.message
    )

@patch('app.services.ban_notification_service.ban_notification_types.BehavioralViolation.send_email')
def test_behavior_notification_email_service_exception(mock_send):
    mock_send.side_effect = Exception("Email service error")
    notification = BehavioralViolation()
    notification.send_email = mock_send
    
    with pytest.raises(Exception) as exc_info:
        notification.notify("test@example.com")
    assert str(exc_info.value) == "Email service error"
