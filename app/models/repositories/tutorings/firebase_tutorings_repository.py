from app.firebase_config import db
from ..repository_helper import safe_execute

class FirebaseTutoringRepository:
    def __init__(self):
        self.collection_name = "tutorings"
    
    def _dict_to_tutoring(self, data):
        # TODO: Consider to enhance this with an ADO pattern or similar.

        """Convierte un diccionario de Firebase a objeto Tutoring"""
        from app.models.repositories.tutorings.repoTutorials import Tutoring  # TODO change to use its own file.
        return Tutoring(
            id_tutoring=data["id"],
            title_tutoring=data["title"],
            id_tutor=data["tutor"],
            subject=data["subject"],
            date=data["date"],
            start_time=data["start_time"],
            description=data["description"],
            method=data["method"],
            capacity=data["capacity"],
            student_list=data.get("student_list", [])
        )

    def get_tutoria_by_id(self, id):
        def operation():
            # Buscar en Firebase donde el campo 'id' sea igual al parámetro
            query = db.collection(self.collection_name).where("id", "==", id).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return self._dict_to_tutoring(doc.to_dict())
            return None

        return safe_execute(operation, fallback=None, context="[get_tutoria_by_id]")