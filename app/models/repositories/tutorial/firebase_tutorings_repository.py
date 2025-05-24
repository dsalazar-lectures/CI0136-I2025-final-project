from app.firebase_config import db
from ..repository_helper import safe_execute

class FirebaseTutoringRepository:
    def __init__(self):
        self.collection_name = "tutorings"
    
    def _dict_to_tutoring(self, data):
        # TODO: Consider to enhance this with an ADO pattern or similar.

        """Convierte un diccionario de Firebase a objeto Tutoring"""
        from app.models.repositories.tutorial.repoTutorials import Tutoring  # TODO change to use its own file.
        return Tutoring(
            id_tutoring=data["id"],
            title_tutoring=data["title"],
            tutor_id=data["tutor_id"],
            tutor=data["tutor"],
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
    
    def get_tutorias_by_tutor(self, tutor_id):
        def operation():
            query = db.collection(self.collection_name).where("tutor_id", "==", tutor_id).get()
            tutorias = []

            for snapshot in query:
                tutorias.append(self._dict_to_tutoring(snapshot.to_dict()))
            
            return tutorias

        return safe_execute(operation, fallback=None, context="[get_tutoria_by_id]")
    
    def get_tutorias_by_student(self, student_id):
        def operation():
            query = db.collection(self.collection_name)
            docs = query.stream()
            tutorias = []

            for snapshot in docs:
                tutoria = snapshot.to_dict()
                if any(s['id'] == student_id for s in tutoria.get("student_list", [])):
                    tutorias.append(self._dict_to_tutoring(tutoria))
            
            return tutorias

        return safe_execute(operation, fallback=None, context="[get_tutoria_by_id]")
