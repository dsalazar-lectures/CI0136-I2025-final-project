from app.firebase_config import db, get_db
from typing import List
from app.services.audit.audit_observer import AuditEvent
from abc import ABC, abstractmethod
from datetime import datetime

class IFirebaseLogRepository:
    @abstractmethod
    def get_logs_in_range(self, start_index: int = 0, count = None) -> List[dict]:
        pass
    
    @abstractmethod
    def save_log(self, log: AuditEvent):
        pass
    
class FirebaseLogRepository(IFirebaseLogRepository):
    def get_logs_in_range(self, start_index: int = 0, count = None) -> List[dict]:
        query = get_db().collection("logs").order_by('timestamp').offset(start_index)
        if count is not None:
            query = query.limit(count)
        return [doc.to_dict() for doc in query.stream()]
    
    def save_log(self, log: AuditEvent):
        object = {
            "timestamp": str(log.timestamp),
            "user": log.user,
            "action_type": log.action_type.value,
            "details": log.details
        }
        get_db().collection("logs").add(object)