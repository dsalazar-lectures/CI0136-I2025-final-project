class Tutoring:
    def __init__(self, id_tutoring, title_tutoring, id_tutor, subject, date, start_time, description, method, capacity, student_list=None):
        self.id = id_tutoring
        self.title = title_tutoring
        self.tutor = id_tutor
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
            Tutoring(1, "Tutoria de C++", "Sergio Brenes", "Programación II", "2025-10-01", 
                    "10:00", "Reforzar lo aprendido sobre C++", "Virtual", 5,
                     student_list=[{"id": "e1", "name": "Carlos Matamoros"}, 
                                            {"id": "e2", "name": "María López"}]),

            Tutoring(2, "Limites", "Alejandro Pacheco", "Cálculo I", "2025-10-05", 
                    "14:00", "Reforzar lo aprendido sobre limites", "Presencial", 10,
                    student_list=[]),
        ]

    def get_tutoria_by_id(self, id):
        for t in self.tutorias:
            if t.id == int(id):
                return t
        return None
