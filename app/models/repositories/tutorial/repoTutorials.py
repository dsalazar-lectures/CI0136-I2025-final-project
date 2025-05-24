from .tutorial import Tutorial
from .ITutorialRepository import ITutorialRepository

class Tutorial_mock_repo(ITutorialRepository): 
    def __init__(self):
        

        self.tutorias = [
            Tutorial(1, "Tutoria de C++", 1, "Juan Pérez", "Programación II", "2025-10-01", 
                    "10:00", "Reforzar lo aprendido sobre C++", "Virtual", 5,
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
