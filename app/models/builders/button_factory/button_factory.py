from app.models.builders.button_factory.buttons.button_zoom import ButtonZoom


class button_factory:
    def __init__(self, button_type):
        self.button_type = button_type

    def create_button(self, meeting_link):
        if self.button_type == "zoom":
             button = ButtonZoom()
             return button.render_access_button(meeting_link)
        else:
            raise ValueError("Unknown button type")