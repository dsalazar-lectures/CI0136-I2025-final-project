from ..models.repoTutorias import Tutoria

def getTutoriaByID():
    return [
        Tutoria(1, "Tutoria de C++", "Sergio Brenes", "Programación II", "2025-10-01", "10:00", "Reforzar lo aprendido sobre C++", "Virtual", 5),
        Tutoria(2, "Limites", "Alejandro Pacheco", "Cálculo I", "2025-10-05", "14:00", "Reforzar lo aprendido sobre limites", "Presencial", 10),
    ]
