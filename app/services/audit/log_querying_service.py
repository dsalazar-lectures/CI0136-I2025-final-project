from typing import List
from app.models.repositories.firebase_log_repository import IFirebaseLogRepository
from app.services.audit.audit_observer import AuditEvent

class LogIterator:
    logs: List[dict]
    log_repository: IFirebaseLogRepository

    def __init__(self, log_repository: IFirebaseLogRepository):
        self.log_repository = log_repository
        
        
    def load_logs(self, start_index: int = 0, count = None ):
        self.logs = self.log_repository.get_logs_in_range(start_index, count)

class LogQueryingService:
    log_iterator: LogIterator

    def __init__(self, log_repository: IFirebaseLogRepository):
        self.log_iterator = LogIterator(log_repository)

    def get_log_page(self, page_number, logs_per_page) -> List[dict]:
        self.log_iterator.load_logs(page_number * logs_per_page, logs_per_page)
        return self.log_iterator.logs

