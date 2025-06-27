from abc import ABC, abstractmethod

class MeetingService(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def create_meeting(self, meeting_data):
        """Create a new meeting with the provided data."""
        pass

    @abstractmethod
    def update_meeting(self, meeting_id, updated_data):
        """Update an existing meeting with the given ID."""
        pass

    @abstractmethod
    def delete_meeting(self, meeting_id):
        """Delete a meeting by its ID."""
        pass

class zoom_meeting_service(MeetingService):
    def create_meeting(self, meeting_data):
        # Implementation for creating a Zoom meeting
        pass

    def update_meeting(self, meeting_id, updated_data):
        # Implementation for updating a Zoom meeting
        pass

    def delete_meeting(self, meeting_id):
        # Implementation for deleting a Zoom meeting
        pass