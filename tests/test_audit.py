import os
import tempfile
import shutil
from datetime import datetime
import pytest
from app.services.audit.audit_types import AuditActionType
from app.services.audit.audit_observer import AuditEvent, AuditObserver, AuditSubject
from app.services.audit.file_audit_observer import FileAuditObserver
from app.services.audit import log_audit

# Test AuditActionType enum
def test_audit_action_type_enum():
    assert AuditActionType.USER_LOGIN.value == "USER_LOGIN"
    assert AuditActionType.CONTENT_CREATE.value == "CONTENT_CREATE"

# Test AuditEvent string representation
def test_audit_event_str():
    event = AuditEvent(
        timestamp=datetime(2024, 1, 1, 12, 0),
        user="alice",
        action_type=AuditActionType.USER_LOGIN,
        details="Logged in successfully"
    )
    s = str(event)
    assert "alice" in s
    assert "user login" in s
    assert "Logged in successfully" in s
    assert "01/01/2024" in s

# Dummy observer for testing
class DummyObserver(AuditObserver):
    def __init__(self):
        self.events = []
    def update(self, event):
        self.events.append(event)

# Test observer attach/detach/notify
def test_audit_subject_observer_pattern():
    subject = AuditSubject()
    observer = DummyObserver()
    subject.attach(observer)
    event = AuditEvent(datetime.now(), "bob", AuditActionType.USER_LOGOUT, "Logged out")
    subject.notify(event)
    assert observer.events[-1] == event
    subject.detach(observer)
    subject.notify(event)
    assert len(observer.events) == 1  # No new event after detach

# Test FileAuditObserver writes to file
def test_file_audit_observer_writes(tmp_path):
    log_dir = tmp_path / "logs"
    observer = FileAuditObserver(str(log_dir))
    event = AuditEvent(datetime(2024, 1, 2, 15, 30), "carol", AuditActionType.USER_REGISTER, "Registered")
    observer.update(event)
    log_files = list(log_dir.glob("audit_log_*.log"))
    assert log_files, "No log file created"
    with open(log_files[0], "r", encoding="utf-8") as f:
        content = f.read()
    assert "carol" in content
    assert "user register" in content
    assert "Registered" in content

# Test log_audit function (integration)
def test_log_audit_function(tmp_path, monkeypatch):
    # Patch the FileAuditObserver to use a temp dir
    from app.services.audit import audit_subject, file_observer
    new_observer = FileAuditObserver(str(tmp_path))
    audit_subject.detach(file_observer)
    audit_subject.attach(new_observer)
    log_audit("dave", AuditActionType.USER_DELETE, "Deleted account")
    log_files = list(tmp_path.glob("audit_log_*.log"))
    assert log_files, "No log file created by log_audit"
    with open(log_files[0], "r", encoding="utf-8") as f:
        content = f.read()
    assert "dave" in content
    assert "user delete" in content
    assert "Deleted account" in content
    # Clean up
    audit_subject.detach(new_observer)
    audit_subject.attach(file_observer) 