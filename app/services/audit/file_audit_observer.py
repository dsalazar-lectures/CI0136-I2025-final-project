import os
from datetime import datetime
from pathlib import Path
from .audit_observer import AuditObserver, AuditEvent
from app.models.repositories.firebase_log_repository import FirebaseLogRepository

class FileAuditObserver(AuditObserver):
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = log_dir
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        Path(self.log_dir).mkdir(parents=True, exist_ok=True)

    def _get_log_file_path(self) -> str:
        current_date = datetime.now().strftime("%Y-%m-%d")
        return os.path.join(self.log_dir, f"audit_log_{current_date}.log")

    def update(self, event: AuditEvent) -> None:
        FirebaseLogRepository().save_log(event)
        log_file = self._get_log_file_path()
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(f"{str(event)}\n") 