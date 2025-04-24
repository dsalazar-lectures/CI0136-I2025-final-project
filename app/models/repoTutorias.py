class Tutoria:
    def __init__(self, id_tutoria, titulo_tutoria, id_tutor, materia, fecha, hora_inicio, descripcion, modalidad, cupo):
        self.id = id_tutoria
        self.titulo = titulo_tutoria
        self.tutor = id_tutor
        self.materia = materia
        self.fecha = fecha
        self.hora_inicio = hora_inicio
        self.descripcion = descripcion
        self.modalidad = modalidad
        self.cupo = cupo

class RepoTutorias:
    def __init__(self):
        self.tutorias = [
            Tutoria(1, "Tutoria de C++", "Sergio Brenes", "Programación II", "2025-10-01", "10:00", "Reforzar lo aprendido sobre C++", "Virtual", 5),
            Tutoria(2, "Limites", "Alejandro Pacheco", "Cálculo I", "2025-10-05", "14:00", "Reforzar lo aprendido sobre limites", "Presencial", 10),
        ]

    def get_tutoria_by_id(self, id):
        for t in self.tutorias:
            if t.id == int(id):
                return t
        return None
