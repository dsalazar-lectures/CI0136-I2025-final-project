from unittest.mock import MagicMock, patch
from unittest import TestCase

with patch("app.firebase_config.db", MagicMock()):
    from app.services.audit.log_querying_service import LogQueryingService, LogIterator

class LogQueryingTests(TestCase):
    def test_get_log_page_doesnt_trow_exceptions(self):
        model = LogQueryingService(MagicMock())
        model.get_log_page(0, 10)
    
    def test_iterator_load_logs_doesnt_trow_exceptions(self):
        iterator = LogIterator(MagicMock())
        iterator.load_logs(0, 10)