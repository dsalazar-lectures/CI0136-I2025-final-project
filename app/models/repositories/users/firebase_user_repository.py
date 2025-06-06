from app.models.services.user_repository_interface import IUserRepository
from app.firebase_config import db
from ..repository_helper import safe_execute

class FirebaseUserRepository(IUserRepository):
    def __init__(self):
        self.collection_name = "users"

    def get_user_by_email(self, email):
        def operation():
            doc = db.collection(self.collection_name).document(email).get()
            return doc.to_dict() if doc.exists else None

        return safe_execute(operation, fallback=None, context="[get_user_by_email]")

    def add_user(self, name, email, password, role):
        def operation():
            users_ref = db.collection(self.collection_name)

            # Gets all users to find the maximum ID and create a new one
            # that is unique. TODO: Optimize this to avoid fetching all users.
            all_users = users_ref.stream()
            max_id = 1
            for user_doc in all_users:
                data = user_doc.to_dict()
                if 'id' in data and isinstance(data['id'], int):
                    max_id = max(max_id, data['id'] + 1)

            new_user = {
                "email": email,
                "name": name,
                "password": password,
                "id": max_id,
                "role": role
            }

            # TODO: Check if the user already exists before adding?
            users_ref.document(email).set(new_user)
            return new_user

        return safe_execute(operation, fallback=None, context="[add_user]")

    def user_exists(self, email):
        def operation():
            doc = db.collection(self.collection_name).document(email).get()
            return doc.exists

        return safe_execute(operation, fallback=False, context="[user_exists]")

    def update_user_fields(self, email, updates):
        allowed_fields = {"name", "role"}
        filtered_updates = {k: v for k, v in updates.items() if k in allowed_fields}

        def operation():
            doc_ref = db.collection(self.collection_name).document(email)
            doc_ref.update(filtered_updates)

        return safe_execute(operation, fallback=None, context="[update_user_fields]")

    def get_all_users(self):
        def operation():
            users_ref = db.collection(self.collection_name)
            all_users_docs = users_ref.stream()
            users_list = [doc.to_dict() for doc in all_users_docs]
            return users_list

        return safe_execute(operation, fallback=[], context="[get_all_users]")

    def update_user_status(self, email, status):
        def operation():
            doc_ref = db.collection(self.collection_name).document(email)
            doc_ref.update({"status": status})
            return True

        return safe_execute(operation, fallback=False, context="[update_user_status]")
    
    def get_user_by_id(self, id):
        def operation():
                users_ref = db.collection(self.collection_name)
                all_users = users_ref.stream()

                for user_doc in all_users:
                    data = user_doc.to_dict()
                    if data and data.get("id") == id:
                        return data
                return None

        return safe_execute(operation, fallback=None, context="[get_user_by_id]")

    def update_user_password(self, email, new_password):
        def operation():
            user_ref = db.collection(self.collection_name).document(email)

            if not user_ref.get().exists:
                return False  # User doesn't exist

            user_ref.update({"password": new_password})
            return True  # update succesfully

        return safe_execute(operation, fallback=False, context="[update_user_password]")
