from app.firebase_config import db
from typing import Callable, Iterable, List
from audit_observer import AuditEvent

class LogIterator:
    logs: List[AuditEvent]
    def __init__(self):
        logs = []
        
    def load_logs_range(
        self,
        start_index: int = 0,
        count = None
    ):
        query = db.collection("logs").order_by('timestamp').offset(start_index)
        if count is not None:
            query = query.limit(count)
        log_objects = [doc.to_dict() for doc in query.stream()]
        for log_object in log_objects:
            log = self.logs.append(AuditEvent())
            for key, value in log_object.items():
                setattr(log, key, value)
        

class LogQueryingService:

    def __init__(self):
        self.log_iterator: LogIterator = LogIterator()

    def get_log_page(self, page_number, logs_per_page) -> List[AuditEvent]:
        self.log_iterator.load_logs_range(page_number * logs_per_page, logs_per_page)
        return self.log_iterator.logs

