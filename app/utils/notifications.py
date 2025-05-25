class NotificationManager:
    def __init__(self):
        self.messages = []

    def add(self, message, category='info'):
        self.messages.append({'message': message, 'category': category})

    def get_all(self):
        msgs = self.messages.copy()
        self.clear()
        return msgs

    def clear(self):
        self.messages = []

# Instancia global
notifier = NotificationManager()
