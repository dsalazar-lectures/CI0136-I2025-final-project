# Logs Framework Manual:

# 1. Overview:
This document describes the usage and structure of the internal logging framework.
Its purpose is to provide a consistent way to track the user and system behavior 
for traceability and audit purposes. It is useful for analytics and debugging 
purposes.


# 2. Importing the Framework:

To include the log framework in a determined module or script, import the 
following packages included in the repository files:

```python
from app.services.audit import log_audit, AuditActionType
```


# 3. Usage Example:

To log a certain action or event after it ocurred, call the `log_audit` function.
You must adjust the function parameters based on the context and conditions of 
the event or action to log.

```python
log_audit("Aaron", AuditActionType.CONTENT_READ, "Home page viewed")
```


**Parameters:**
1) User: Name of the user that made an action.
2) Action Type: Action made by the user, defined in `audit_types.py` enum.
3) Details: Free-text field for describing the action or event logged.

**Note:** A Timestamp is auto-generated and included in a log after calling `log_audit`.
It Represents the exact date and time when the action occurred (`datetime.now()` format).


Log output example (CLI, GUI or text file):
```python
Aaron content read at 24/04/2025 07:46 AM - Home page viewed
```


# 4. AuditEvent Structure:

All log entries are encapsulated as `AuditEvent` objects.

```python
@dataclass
class AuditEvent:
    timestamp: datetime
    user: str
    action_type: AuditActionType
    details: str
```


## 5. Storage & Retention  

All audit logs are stored as plain text files in the `/logs` directory of the application.  

### File Naming Convention  
- A new log file is created daily with the format:  


```python
audit_log_YYYY-MM-DD.log
```


### Retention Policy  
- Logs are appended to the current day's file  
- Historical logs are preserved indefinitely (no automatic deletion)  


# 6. Good Practices:

- Use consistent details strings for similar actions (e.g., “Viewed Dashboard” vs “Dashboard viewed”).
- Never include sensitive user data (e.g., passwords, tokens) in log details.
- Always log meaningful actions that help trace user behavior or system issues.