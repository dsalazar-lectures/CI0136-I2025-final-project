from .audit_types import AuditActionType
from .audit_observer import AuditSubject
from .file_audit_observer import FileAuditObserver

# Create and configure the audit system
audit_subject = AuditSubject()
file_observer = FileAuditObserver()
audit_subject.attach(file_observer)

# Export the main logging function
def log_audit(user: str, action_type: AuditActionType, details: str) -> None:
    """
    Log an audit event.
    
    Args:
        user (str): The user performing the action
        action_type (AuditActionType): The type of action being performed
        details (str): Additional details about the action
    """
    audit_subject.log(user, action_type, details) 