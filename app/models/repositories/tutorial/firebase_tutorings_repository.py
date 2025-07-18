from app.firebase_config import db
from ..repository_helper import safe_execute
from .ITutorialRepository import ITutorialRepository
import uuid

class FirebaseTutoringRepository(ITutorialRepository):
    def __init__(self):
        self.collection_name = "tutorings"
    
    def _dict_to_tutoring(self, data):
        # TODO: Consider to enhance this with an ADO pattern or similar.

        """Convierte un diccionario de Firebase a objeto Tutoring"""
        from app.models.repositories.tutorial.repoTutorials import Tutorial  # TODO change to use its own file.
        return Tutorial(
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
            student_list=data.get("student_list", []),
            meeting_link=data.get("meeting_link"),
        )

    def get_tutorial_by_id(self, id):
        def operation():
            # Buscar en Firebase donde el campo 'id' sea igual al parámetro
            query = db.collection(self.collection_name).where("id", "==", id).limit(1)
            docs = query.stream()
            
            for doc in docs:
                return self._dict_to_tutoring(doc.to_dict())
            return None

        return safe_execute(operation, fallback=None, context="[get_tutoria_by_id]")
    
    def get_tutorials_by_tutor(self, tutor_id):
        def operation():
            query = db.collection(self.collection_name).where("tutor_id", "==", tutor_id).get()
            tutorias = []

            for snapshot in query:
                tutorias.append(self._dict_to_tutoring(snapshot.to_dict()))
            
            return tutorias

        return safe_execute(operation, fallback=None, context="[get_tutoria_by_id]")
    
    def get_tutorials_by_student(self, student_id):
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
    
    def get_list_tutorials(self):
        def operation():
            # Obtener todas las tutorías desde Firebase
            query = db.collection(self.collection_name).stream()
            tutorials = []

            for snapshot in query:
                tutorial_data = snapshot.to_dict()
                # print("Datos recuperados de Firebase:", tutorial_data)

                tutoring_obj = self._dict_to_tutoring(tutorial_data)
                # print("Resultado de _dict_to_tutoring:", tutoring_obj)

                if tutoring_obj:
                    tutorials.append(tutoring_obj)
                else:
                    print("⚠ Se ignoró un tutorial por conversión fallida")

            return tutorials

        return safe_execute(operation, fallback=[], context="[get_list_tutorials]")
    
    def register_in_tutoria(self, id_student, name_student, id_tutoria):
        def operation():
            # Obtiene una tutoria por su ID
            tutoria_ref = db.collection(self.collection_name).where("id", "==", id_tutoria).limit(1)
            docs = tutoria_ref.stream()
            
            for doc in docs: # Solo debería haber un documento, porque las tutorias son unicas
                tutoria = doc.to_dict()
                doc_id = doc.id  # Firebase document ID
                
                # Verificar si hay cupos disponibles
                if tutoria["capacity"] == len(tutoria.get("student_list", [])):
                    print("No hay cupos disponibles")
                    return False
                
                # Verificar si el estudiante ya está registrado
                for student in tutoria.get("student_list", []):
                    if student["id"] == id_student:
                        print("El estudiante ya está registrado")
                        return False
                
                # Registrar al estudiante
                tutoria["student_list"].append({"id": id_student, "name": name_student})
                db.collection(self.collection_name).document(doc_id).update({"student_list": tutoria["student_list"]})
                print("Estudiante registrado")
                return True
            
            print("Tutoria no encontrada")
            return False

        return safe_execute(operation, fallback=False, context="[register_in_tutoria]")
    
    def create_tutorial(self, title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity):
        def operation():
            new_id = str(uuid.uuid4())
            new_tutoring = {
                "id": new_id,
                "title": title_tutoring,
                "tutor_id": tutor_id,
                "tutor": tutor,
                "subject": subject,
                "date": date,
                "start_time": start_time,
                "description": description,
                "method": method,
                "capacity": capacity,
                "student_list": []
            }

            db.collection(self.collection_name).document(new_id).set(new_tutoring)
            return new_tutoring

        return safe_execute(operation, fallback=None, context="[create_tutorial]")

    def update_tutorial(self, id, updated_data):
            def operation():
                # Buscar el documento por el campo 'id'
                query = db.collection(self.collection_name).where("id", "==", id).limit(1)
                docs = query.stream()
                for doc in docs:
                    doc_id = doc.id  # ID interno de Firestore
                    db.collection(self.collection_name).document(doc_id).update(updated_data)
                    return True
                return False  # No encontrado

            return safe_execute(operation, fallback=False, context="[update_tutorial]")

    def cancel_tutorial(self, tutorial_id):
        def operation():
            # Find the tutorial document by ID
            query = db.collection(self.collection_name).where("id", "==", tutorial_id).limit(1)
            docs = query.stream()
            
            for doc in docs:
                # Delete the document
                db.collection(self.collection_name).document(doc.id).delete()
                return True
            
            return False

        return safe_execute(operation, fallback=False, context="[cancel_tutorial]")

    def unregister_from_tutoria(self, student_id, tutoria_id):
        def operation():
            # Buscar la tutoría por ID
            query = db.collection(self.collection_name).where("id", "==", tutoria_id).limit(1)
            docs = query.stream()
            
            for doc in docs:
                tutoria = doc.to_dict()
                doc_id = doc.id
                
                # Verificar si el estudiante está inscrito
                if not any(s["id"] == student_id for s in tutoria.get("student_list", [])):
                    return False
                    
                # Crear nueva lista sin el estudiante
                new_student_list = [s for s in tutoria["student_list"] if s["id"] != student_id]
                
                # Actualizar en Firebase
                db.collection(self.collection_name).document(doc_id).update({
                    "student_list": new_student_list
                })
                return True
            
            return False  # Tutoría no encontrada

        return safe_execute(operation, fallback=False, context="[unregister_from_tutoria]")