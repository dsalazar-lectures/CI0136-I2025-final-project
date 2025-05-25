from app.firebase_config import db, get_db
from typing import Callable, Iterable, List
from app.services.audit.audit_observer import AuditEvent, AuditActionType
from abc import ABC, abstractmethod
from datetime import datetime

class IFirebaseLogRepository:
    @abstractmethod
    def get_logs_in_range(self, start_index: int = 0, count = None) -> List[AuditEvent]:
        pass
    
    @abstractmethod
    def save_log(self, log: AuditEvent):
        pass
    
class FirebaseLogRepository(IFirebaseLogRepository):
    def get_logs_in_range(self, start_index: int = 0, count = None) -> List[AuditEvent]:
        logs: List[AuditEvent] = []
        query = get_db().collection("logs").order_by('timestamp').offset(start_index)
        if count is not None:
            query = query.limit(count)
        log_objects: List[dict] = [doc.to_dict() for doc in query.stream()]
        for log_object in log_objects:
            log: AuditEvent = logs.append(AuditEvent(log_object["timestamp"], log_object["user"], log_object["action_type"], log_object["details"]))
        return logs
    
    def save_log(self, log: AuditEvent):
        object = {
            "timestamp": str(log.timestamp),
            "user": log.user,
            "action_type": log.action_type.value,
            "details": log.details
        }
        get_db().collection("logs").add(object)