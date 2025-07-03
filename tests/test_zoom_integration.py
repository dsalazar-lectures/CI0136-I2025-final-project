import unittest
from unittest.mock import patch
from app.services.meetings.zoom_meeting_service import zoom_meeting_service

class TestZoomMeetingService(unittest.TestCase):
    @patch('app.services.meetings.zoom_meeting_service.requests.post')
    def test_create_meeting_success(self, mock_post):
        # Simula respuesta exitosa de Zoom
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = {
            "join_url": "https://zoom.us/j/123456789"
        }
        service = zoom_meeting_service()
        access_token = "fake_token"
        meeting_data = {
            "topic": "Test",
            "start_time": "2025-07-02T10:00:00Z",
            "duration": 60
        }
        response = service.create_meeting(access_token, meeting_data)
        self.assertEqual(response["join_url"], "https://zoom.us/j/123456789")

    @patch('app.services.meetings.zoom_meeting_service.requests.post')
    def test_create_meeting_failure(self, mock_post):
        mock_post.return_value.status_code = 400
        mock_post.return_value.text = "Bad Request"
        service = zoom_meeting_service()
        access_token = "fake_token"
        meeting_data = {}
        with self.assertRaises(Exception):
            service.create_meeting(access_token, meeting_data)

if __name__ == '__main__':
    unittest.main()