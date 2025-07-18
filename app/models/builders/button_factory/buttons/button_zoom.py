from app.models.builders.button_factory.button_link import ButtonLink
from app.models.repositories.tutorial.firebase_tutorings_repository import FirebaseTutoringRepository 

class ButtonZoom(ButtonLink):
        
    def render_access_button(self, meeting_link):
        tutoring_link = meeting_link
        
        if tutoring_link:
            return f'<a href="{tutoring_link}" class="btn btn-primary" target="_blank">Join Zoom Meeting</a>'
        