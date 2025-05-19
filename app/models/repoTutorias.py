class Tutoring:
    def __init__(self, id_tutoring, title_tutoring, tutor_id, tutor, subject, date, start_time, description, method, capacity, student_list=None):
        self.id = id_tutoring
        self.title = title_tutoring
        self.tutor = tutor
        self.tutor_id = tutor_id
        self.subject = subject
        self.date = date
        self.start_time = start_time
        self.description = description
        self.method = method
        self.capacity = capacity
        self.student_list = student_list if student_list else []

class RepoTutoring:
    def __init__(self):
        

        self.tutorias = [
            Tutoring(1, "Tutoria de C++", 1, "Programación II", "2025-10-01", 
                    "10:00", "Reforzar lo aprendido sobre C++", "Virtual", 5,
                     student_list=[{"id": "e1", "name": "Carlos Matamoros"}, 
                                            {"id": "e2", "name": "María López"}]),

            Tutoring(2, "Limites", 2, "Cálculo I", "2025-10-05", 
                    "14:00", "Reforzar lo aprendido sobre limites", "Presencial", 10,
                    student_list=[]),
        ]

    def get_tutoria_by_id(self, id):
        for t in self.tutorias:
            if t.id == int(id):
                return t
        return None
    
    def get_tutorias_by_tutor(self, tutor_id):
        return [t for t in self.tutorias if t.tutor_id == tutor_id]
