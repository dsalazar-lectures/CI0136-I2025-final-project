from .tutorial import Tutorial
from .ITutorialRepository import ITutorialRepository

class Tutorial_mock_repo(ITutorialRepository): 
    def __init__(self):
        

        self.tutorias = [
            Tutorial(1, "Tutoria de C++", 1, "Juan Pérez", "Programación II", "2025-10-01", 
                    "10:00", "Reforzar lo aprendido sobre C++", "Virtual", 1,
                     student_list=[{"id": 1, "name": "Carlos Matamoros"}, 
                                            {"id": 2, "name": "María López"}]),

            Tutorial(2, "Limites", 2, "Ana Gómez", "Cálculo I", "2025-10-05", 
                    "14:00", "Reforzar lo aprendido sobre limites", "Presencial", 10,
                    student_list=[]),
        ]

    def get_tutorial_by_id(self, id):
        for t in self.tutorias:
            if t.id == int(id):
                return t
        return None
    
    def get_tutorias_by_tutor(self, tutor_id):
        return [t for t in self.tutorias if t.tutor_id == tutor_id]
    
    def get_tutorias_by_student(self, student_id):
        return [t for t in self.tutorias 
                if any(s['id'] == student_id for s in t.student_list)]
    
    def create_tutorial(self, title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity):
        new_id = max(t.id for t in self.tutorias) + 1
        new_tutoring = Tutorial(
            new_id, 
            title_tutoring, 
            tutor_id,
            tutor,
            subject, 
            date, 
            start_time, 
            description, 
            method, 
            capacity
        )
        self.tutorias.append(new_tutoring)
        return new_tutoring
    
    def update_tutorial(self, id, updated_data):
        tutorial = self.get_tutorial_by_id(id)
        if tutorial:
            tutorial.title = updated_data.get('title_tutoring', tutorial.title)
            tutorial.subject = updated_data.get('subject', tutorial.subject)
            tutorial.date = updated_data.get('date', tutorial.date)
            tutorial.start_time = updated_data.get('start_time', tutorial.start_time)
            tutorial.description = updated_data.get('description', tutorial.description)
            tutorial.method = updated_data.get('method', tutorial.method)
            tutorial.capacity = updated_data.get('capacity', tutorial.capacity)
            return True
        return False
    
    def list_tutorials(self):
        return self.tutorias
    
    def register_in_tutoria(self, id_student, name_student, id_tutoria):
        resgister = False  # Inicializar la variable
        tutoria = self.get_tutorial_by_id(id_tutoria)
        if tutoria.capacity == len(tutoria.student_list):
            print("No hay cupos disponibles")
        else:
            for student in tutoria.student_list:
                if student["id"] == id_student:
                    print("El estudiante ya está registrado")
                    resgister = False
                    break
            else:  # Este bloque se ejecuta si no se rompe el bucle
                tutoria.student_list.append({"id": id_student, "name": name_student})
                print("Estudiante registrado")
                resgister = True
        return resgister

    def list_tutor_tutorials(self, tutor_id, search=None, sort=None):
            if not tutor_id:
                return []
            
            tutorias = self.get_tutorias_by_tutor(tutor_id)
            
            if search:
                search = search.lower()
                tutorias = [t for t in tutorias if search in t.title.lower() or search in t.subject.lower()]
            
            if sort == 'asc':
                tutorias.sort(key=lambda t: t.date)
            elif sort == 'desc':
                tutorias.sort(key=lambda t: t.date, reverse=True)
            
            return tutorias