from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from dataclasses import dataclass
from .audit_types import AuditActionType

@dataclass
class AuditEvent:
    timestamp: datetime
    user: str
    action_type: AuditActionType
    details: str
    
    def __str__(self) -> str:
        return f"{self.user} {self.action_type.value.lower().replace('_', ' ')} at {self.timestamp.strftime('%d/%m/%Y %I:%M %p')} - {self.details}"

class AuditObserver(ABC):
    @abstractmethod
    def update(self, event: AuditEvent) -> None:
        """Handle the audit event."""
        pass

class AuditSubject:
    _observers: List[AuditObserver] = []
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuditSubject, cls).__new__(cls)
        return cls._instance

    def attach(self, observer: AuditObserver) -> None:
        if observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer: AuditObserver) -> None:
        self._observers.remove(observer)

    def notify(self, event: AuditEvent) -> None:
        for observer in self._observers:
            observer.update(event)

    def log(self, user: str, action_type: AuditActionType, details: str) -> None:
        event = AuditEvent(
            timestamp=datetime.now(),
            user=user,
            action_type=action_type,
            details=details
        )
        self.notify(event) 