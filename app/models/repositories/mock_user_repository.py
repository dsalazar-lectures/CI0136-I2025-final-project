from ..services.user_repository_interface import IUserRepository

class MockUserRepository(IUserRepository):
    def __init__(self):
        self.users = {
            "admin@example.com": {
                "password": "Admin1@",
                "id": 1,
                "role": "Student"
            }
        }
        self.next_id = 2

    def get_user_by_email(self, email):
        return self.users.get(email)

    def add_user(self, email, password, role):
        self.users[email] = {
            "password": password,
            "id": self.next_id,
            "role": role
        }
        self.next_id += 1

    def user_exists(self, email):
        return email in self.users
