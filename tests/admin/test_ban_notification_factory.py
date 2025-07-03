import pytest
from app.services.ban_notification_service.ban_notification_types import BanNotificationFactory, BehavioralViolation

def test_create_ban_notification_behavior_type():
    notification = BanNotificationFactory.create_ban_notification("behavior")
    assert isinstance(notification, BehavioralViolation)

def test_create_ban_notification_invalid_type():
    with pytest.raises(ValueError):
        BanNotificationFactory.create_ban_notification("invalid_type")

def test_create_ban_notification_none_type():
    with pytest.raises(ValueError):
        BanNotificationFactory.create_ban_notification(None)
