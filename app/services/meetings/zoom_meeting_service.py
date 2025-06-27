from app.services.meetings.meeting_service import MeetingService
from flask import redirect
import base64
import requests

class zoom_meeting_service(MeetingService):
    def __init__(self):
        self.CLIENT_ID = 'F3ehaqQxSAWQbHbGC0SiLA'
        self.CLIENT_SECRET = '52yDb1pALIQbh4os4J7VHfMvYPM43a9x'
        self.REDIRECT_URI = 'http://localhost:5000/zoom/callback'
        
    
    def create_meeting(self, meeting_data):
        
        pass

    def update_meeting(self, meeting_id, updated_data):
        # Implementation for updating a Zoom meeting
        pass

    def delete_meeting(self, meeting_id):
        # Implementation for deleting a Zoom meeting
        pass

    def connect_to_zoom(self):
        zoom_auth_url = (
        f"https://zoom.us/oauth/authorize?response_type=code"
        f"&client_id={self.CLIENT_ID}"
        f"&redirect_uri={self.REDIRECT_URI}"
        )
        return redirect(zoom_auth_url)
    
    def handle_zoom_callback(self, code):
        auth_str = f"{self.CLIENT_ID}:{self.CLIENT_SECRET}"
        auth_b64 = base64.b64encode(auth_str.encode()).decode()

        headers = {
            "Authorization": f"Basic {auth_b64}",
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.REDIRECT_URI
        }

        response = requests.post("https://zoom.us/oauth/token", headers=headers, data=data)

        if response.status_code == 200:
            return response.json()  # contiene el access_token, refresh_token, etc.
        else:
            raise Exception(f"Error al obtener token de Zoom: {response.text}")